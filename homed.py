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
__version__ = '0.7'


import asyncio
import signal
import importlib
import sys
import json
import logging
from threading import Thread, current_thread, RLock, enumerate
from time import sleep
from couchdb import Server
sys.path.append('/etc/smarthouse')


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
        self.config = {"user": "homedaemon",
                       "password": "devpas",
                       "dbname": "homedamondb",
                       "addr": "localhost"}
        self.loop = asyncio.get_event_loop()
        self.buffer_size = 1024
        self.events = dict()
        self.inputs = dict()
        self.inputs_list = [
            # 'dummy',
            'gateway',
            # 'arduino',
            'tcp',
            'websocket',
            'yeelight'
        ]
        self.event_list = [
            'heartbeat',
            'report',
            'write']
        self.queue = Queue()
        self.db = Server()
        self.devices = self.db['devices']
        self.device_data = self.db['devices-data']
        self.logger = logging
        self.logger.basicConfig(filename='homed.log',
                                filemode='w',  # TODO: change to 'a' in production mode
                                format='%(asctime)s %(levelname)s:%(message)s',
                                datefmt='%m/%d/%Y %H:%M:%S',
                                level=logging.INFO)
        self.logger.info('Starting Daemon')
        self.token = None
        self.workers = list()

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
            inst = _input.Input(self.queue)
            self.inputs[inst.name] = inst
            self.logger.info(f'load input: {inst.name}')
            self.inputs[inst.name].start()

    def _queue_put(self, item):
        if type(item) is not dict:
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                self.logger.warning(f'Wrong data: {item}')
                return
        self.queue.put(item)

    def _load_events(self):
        """loadEvents"""
        for event in self.event_list:
            ev = importlib.import_module(f'homedaemon.events.{event}')
            inst = ev.Event(self)
            self.events[inst.name] = inst
            self.logger.info(f'Load event: {inst.name}')

    def run(self):
        print(f'main thread {current_thread()} loop {id(self.loop)}')
        self._load_events()
        self._load_inputs()
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        watcher = Thread(name='watcher', target=self.event_watcher)
        self.loop.call_later(0.5, watcher.start)

        try:
            self.logger.info('Daemon is listening')
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def stop(self, *args, **kwargs):
        print('Stop')
        self.loop.stop()
        # self.loop.close()

    def event_watcher(self):
        """This method is """
        print(f'Waching Queue {current_thread()}')
        while self.loop.is_running():
            if self.queue.empty():
                sleep(0.1)
                continue
            data = self.queue.get()
            if type(data) is not dict:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    self.logger.warning(f'Wrong data: {data}')
                    return
            event_name = data.get('cmd')
            ev = self.events.get(event_name)
            if ev:
                ev.do(data)
            else:
                self.logger.error(f'Unknown event: {data}')
        print('Stop watching')


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()

