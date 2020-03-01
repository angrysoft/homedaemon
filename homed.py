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
from threading import Thread, current_thread, RLock
from time import sleep
from pycouchdb import Server
from systemd.journal import JournalHandler
from homedaemon.devices import Devices
from homedaemon.bus import Bus
from asyncio import tasks
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger('homed')


class HomeDaemon:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.inputs = dict()
        self.bus = Bus(self.loop)
        # self.bus.start()
        self.db = Server()
        self.config = self.db['config']
        self.devicesdb = self.db['devices']
        self.device_data = self.db['devices-data']
        self.scenesdb = None
        self.logger = logger
        self.logger.info('Starting Daemon')
        self.devices = Devices()
        self.scenes = dict()
        self.bus.on('report', '*', self.logger.debug)
        self.executors = None

    def _load_inputs(self):
        # self.executors = ThreadPoolExecutor()
        for _input_name in self.config['inputs']['list']:
            _input = importlib.import_module(f'homedaemon.inputs.{_input_name}')
            inst = _input.Input(self.bus, self.config, self.loop)
            self.inputs[inst.name] = inst
            self.logger.info(f'load input: {inst.name}')
            self.inputs[inst.name].run()
            # self.executors.submit(self.inputs[inst.name].run)

    def _load_devices(self):
        for dev in self.devicesdb:
            self.devices.load(dev, self)

    def _load_scenes(self):
        if 'scenes' in self.db:
            self.db.delete('scenes')
        self.db.create('scenes')
        self.scenesdb = self.db['scenes'] 
        sys.path.append(self.config['scenes']['path'])
        with os.scandir(self.config['scenes']['path']) as it:
            for entry in it:
                if entry.name.endswith('.py') and entry.is_file():
                    _scene = importlib.import_module(entry.name[:-3])
                    inst = _scene.Scene(self)
                    if inst.name not in self.scenes:
                        self.scenes[inst.name] = inst
                        self.scenesdb[inst.name] = {'automatic': inst.automatic,
                                                    'name': inst.name,
                                                    'sid': inst.name,
                                                    'reversible': inst.reversible,
                                                    'place': inst.place}
                    else:
                        self.logger.warning(f'scene duplcate name skiping ... {inst.name}')
                        continue
                    self.logger.info(f'loaded {inst.name}')
        self.loop.call_later(5, self._announce_scene_list)
        
    def _announce_scene_list(self):
        sc_list = list()
        for s in self.scenesdb:
            if s.get('automatic') == False:
                del s['_rev']
                sc_list.append(s)
        self.bus.emit_cmd({'cmd': 'scene', 'sid': 'all', 'data': {'scenes': sc_list}})

    def run(self):
        self.logger.info(f'main thread {current_thread()} loop {id(self.loop)}')
        self._load_devices()
        self._load_scenes()
        self._load_inputs()
        # self.loop.add_signal_handler(signal.SIGINT, self.stop)
        # self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        # self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        # self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        try:
            self.logger.debug('Daemon is listening')
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
        self.loop.stop()
    
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
        logging.basicConfig(filename="home.log")
    
    hd = HomeDaemon()
    hd.run()
