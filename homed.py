#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# homed.py
# Copyright (C) 2014-2019  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

__author__ = 'Sebastian Zwierzchowski'
__copyright__ = 'Copyright 2014-2019 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.9'


import asyncio
import signal
import importlib
import json
import os
import sys
import logging
from threading import current_thread
from time import sleep
from pycouchdb import Server
from systemd.journal import JournalHandler
from homedaemon.devices import Devices
from homedaemon.bus import Bus
from asyncio import tasks

logger = logging.getLogger('homed')


class HomeDaemon:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        print(self.loop.get_debug())
        self.inputs = dict()
        self.bus = Bus(self.loop)
        self.db = Server()
        self.config = self.db['config']
        sys.path.append(self.config['scenes']['path'])
        self.devicesdb = self.db['devices']
        self.logger = logger
        self.logger.info('Starting Daemon')
        self.devices = Devices()
        self.bus.add_trigger('report.*.*.*', self.debug)

    def debug(self, msg=None):
        if msg is not None:
            self.logger.debug(f'>>> {msg}')

    def load_inputs(self):
        for _input_name in self.config['inputs']['list']:
            _input = importlib.import_module(f'homedaemon.inputs.{_input_name}')
            inst = _input.Input(self.bus, self.config, self.loop)
            self.inputs[inst.name] = inst
            self.logger.info(f'load input: {inst.name}')
            self.inputs[inst.name].run()

    def load_devices(self):
        dev_list = list()
        for dev in self.devicesdb:
            if self.devices.register(dev, self):
                dev_list.append({'sid': dev['sid'], 'model': dev['model'],
                                'name': dev['name'], 'place': dev['place'],
                                'status': self.devices[dev['sid']].device_status()})
        
        self.bus.emit('report.homed.devices.loaded')
        self.loop.call_later(5, self.bus.emit, 'devices_list.daemon.populate.list', {'cmd':'devices_list', 'data': dev_list})

    def run(self):
        self.debug(f'main thread {current_thread()} loop {id(self.loop)}')
        self.loop.run_in_executor(None, self.load_inputs)
        self.loop.run_in_executor(None, self.load_devices)
        
        # self.loop.add_signal_handler(signal.SIGINT, self.stop)
        # self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        # self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        # self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        try:
            self.bus.emit('report.homed.status.started')
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            try:
                self._cancel_all_tasks()
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            finally:
                self.loop.close()

    def stop(self, *args, **kwargs):
        self.logger.info('Stop homed')
        try:
            self.loop.stop()
            self._cancel_all_tasks()
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        finally:
            self.loop.close()
    
    def _cancel_all_tasks(self):
        to_cancel = tasks.all_tasks(self.loop)
        if not to_cancel:
            return

        for task in to_cancel:
            task.cancel()

        self.loop.run_until_complete(
            tasks.gather(*to_cancel, loop=self.loop, return_exceptions=True))

        for task in to_cancel:
            if task.cancelled():
                continue
            if task.exception() is not None:
                self.loop.call_exception_handler({
                    'message': 'unhandled exception during asyncio.run() shutdown',
                    'exception': task.exception(),
                    'task': task,
                })


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    
    if len(sys.argv) < 2:
        logger.addHandler(JournalHandler())    
    else:
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.addHandler(logging.FileHandler('home.log'))
    
    hd = HomeDaemon()
    hd.run()
