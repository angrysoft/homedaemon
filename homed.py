#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# homed.py
# Copyright (C) 2014-2020  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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

__author__ = 'Angrysoft - Sebastian Zwierzchowski'
__copyright__ = 'Copyright 2014-2020 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.9.1'


import sys
import signal
import asyncio

import importlib
from threading import current_thread
from pycouchdb import Server

from homedaemon.devices import Devices
from homedaemon.bus import Bus
from homedaemon.logger import Logger
from homedaemon.config import *
import argparse


class HomeDaemon:
    def __init__(self, config):
        self.config = config
        self.logger = Logger(debug=args.debug, std=args.log_to_stdout)
        self.loop = asyncio.get_event_loop()
        self.inputs = dict()
        self.bus = Bus(self.loop)
        self.db = Server()
        self.devicesdb = self.db['devices']
        self.logger.info('Starting Daemon')
        self.devices = Devices()
        self.bus.add_trigger('*.*.*.*', self.logger.debug)

    def load_inputs(self):
        for _input_name in self.config['inputs']:
            _input = importlib.import_module(f'homedaemon.inputs.{_input_name}')
            inst = _input.Input(self.bus, self.config, self.loop)
            self.inputs[inst.name] = inst
            self.logger.info(f'load input: {inst.name}')
            self.inputs[inst.name].run()

    def load_devices(self):
        # dev_list = list()
        # for dev in self.devicesdb:
        #     if self.devices.register(dev, self):
        #         dev_list.append({'sid': dev['sid'], 'model': dev['model'],
        #                         'name': dev['name'], 'place': dev['place'],
        #                         'status': self.devices[dev['sid']].device_status()})
        loaded_devices = self.devices.register_devices(self.devicesdb.get_all_docs(), self)
        self.bus.emit('report.homed.devices.loaded')
        # self.loop.call_later(5, self.bus.emit, 'devices_list.daemon.populate.list', {'cmd':'devices_list', 'data': dev_list})
        
    def run(self):
        self.logger.debug(f'main thread {current_thread()} loop {id(self.loop)}')
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

    # def stop(self, *args, **kwargs):
    #     self.logger.info('Stop homed')
    #     try:
    #         self.loop.stop()
    #         self._cancel_all_tasks()
    #         self.loop.run_until_complete(self.loop.shutdown_asyncgens())
    #     finally:
    #         self.loop.close()
    
    def _cancel_all_tasks(self):
        to_cancel = asyncio.tasks.all_tasks(self.loop)
        if not to_cancel:
            return

        for task in to_cancel:
            task.cancel()

        self.loop.run_until_complete(
            asyncio.tasks.gather(*to_cancel, loop=self.loop, return_exceptions=True))

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
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('-d', '--debug', action="store_true", help="Debug msg")
    parser.add_argument('-s', '--log-to-stdout', action="store_true", help="Print log info to stdout")
    parser.add_argument('-c', '--config-dir', nargs='?', default='/etc/angryhome/conf.d', help='Path to config dir')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    
    config = Config()
    config.load_config(JsonConfig(args.config_dir))
    # config.load_config(DbConfig())
    config.load_config(ArgConfig(args))
    print(config)
    hd = HomeDaemon(config)
    hd.run()
   
