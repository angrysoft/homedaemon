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
__version__ = '0.8'


import asyncio
import signal
import importlib
import json
import os
import logging
from threading import Thread, current_thread, RLock
from time import sleep
from couchdb import Server
from systemd.journal import JournalHandler
from homedaemon.devices import Device
from homedaemon.scenes import Scene


class Queue:
    def __init__(self):
        self._queue = list()
        self.lock = RLock()

    def put(self, item):
        with self.lock:
            self._queue.append(item)

    def get(self):
        if self._queue:
            with self.lock:
                return self._queue.pop(0)
        else:
            return None

    def empty(self):
        if self._queue:
            return False
        else:
            return True


class HomeDaemon:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.inputs = dict()
        self.inputs_list = [
            # 'dummy',
            'gateway',
            'arduino',
            'tcp',
            'websocket',
            'yeelight'
        ]
        self.queue = Queue()
        self.db = Server()
        self.config = self.db['config']
        self.devicesdb = self.db['devices']
        self.device_data = self.db['devices-data']
        self.logger = logging.getLogger('homed')
        self.logger.addHandler(JournalHandler())
        self.logger.setLevel(logging.DEBUG)
        self.logger.info('Starting Daemon')
        self.token = None
        self.workers = dict()

    def notify_clients(self, msg):
        if 'websocket' in self.inputs:
            asyncio.run(self.inputs['websocket'].send(msg))

    # async def timers(self):
    #     while True:
    #         self._queue_put({'cmd': 'timers', 'data': 'all'})
    #         await asyncio.sleep(60)

    def _load_inputs(self):
        for _input_name in self.inputs_list:
            _input = importlib.import_module(f'homedaemon.inputs.{_input_name}')
            inst = _input.Input(self.queue, self.config)
            self.inputs[inst.name] = inst
            self.logger.info(f'load input: {inst.name}')
            self.inputs[inst.name].start()

    def _load_devices(self):
        for dev in self.devicesdb:
            self.workers[dev] = Device(self.devicesdb.get(dev), self)

    def _load_scenes(self):
        path = self.config['scenes']['path']
        for sc in os.listdir(path):
            scene = Scene(os.path.join(path, sc), self.queue.put)
            self.workers[scene.name] = scene

    def run(self):
        self.logger.info(f'main thread {current_thread()} loop {id(self.loop)}')
        self._load_devices()
        self._load_scenes()
        self._load_inputs()
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        watcher = Thread(name='watcher', target=self.devices_watcher)
        self.loop.call_later(0.5, watcher.start)

        try:
            self.logger.info('Daemon is listening')
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def stop(self, *args, **kwargs):
        self.logger.info('Stop homed')
        self.loop.stop()

    def devices_watcher(self):
        """This method is """
        self.logger.info(f'Waching Queue {current_thread()}')
        while self.loop.is_running():
            if self.queue.empty():
                sleep(0.1)
                continue
            data = self.queue.get()
            self.logger.info(data)
            if type(data) is not dict:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    self.logger.warning(f'Wrong data: {data}')
                    return
            sid = data.get('sid')
            if sid in self.workers:
                self.workers[sid].do(data)
            else:
                self.logger.error(f'Unknown sid: {data}')
        self.logger.info('Stop watching')


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()

