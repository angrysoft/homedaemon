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
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, current_thread
from time import sleep
from pymongo import MongoClient
sys.path.append('/etc/smarthouse')


class HomeDaemon:
    def __init__(self):
        self.config = {"user": "homedaemon",
                       "password": "devpas",
                       "dbname": "homedamondb",
                       "addr": "localhost"}
        self.server = None
        self.loop = asyncio.get_event_loop()
        self.buffer_size = 1024
        self.transport = None
        self.protocol = None
        self.peername = ''
        self.events = dict()
        self.inputs = dict()
        self.inputs_list = [
            # 'gateway',
            # 'arduino',
            'tcp',
            'websocket',
            'yeelight'
        ]
        self.event_list = [
            # 'heartbeat',
            'report',
            'write']
        self.queue = Queue()
        # self.queue = asyncio.Queue()
        self.cli = MongoClient()
        self.db = self.cli.homedaemondb
        self.devices = self.db.devices
        self.device_data = self.db.devices_data
        self.logger = logging
        self.logger.basicConfig(filename='homed.log',
                                filemode='w',  # TODO: change to 'a' in production mode
                                format='%(asctime)s %(levelname)s:%(message)s',
                                datefmt='%m/%d/%Y %H:%M:%S',
                                level=logging.INFO)
        self.logger.info('Starting Daemon')
        self.token = None
        self.workers = set()

    def notify_clients(self, msg):
        if 'websocket' in self.inputs:
            self.inputs['websocket'].send(msg)

    async def timers(self):
        while True:
            self._queue_put({'cmd': 'timers', 'data': 'all'})
            await asyncio.sleep(60)

    def _load_input(self, input_name):
        _input = importlib.import_module(f'homedaemon.inputs.{input_name}')
        inst = _input.Input(self._queue_put)
        self.inputs[inst.name] = inst
        self.logger.info(f'load input: {inst.name}')
        self.inputs[inst.name].listen()

    def _listen_inputs(self):
        with ThreadPoolExecutor() as e:
            for _input in self.inputs_list:
                print(f'{_input}')
                self.workers.add(e.submit(self._load_input, _input))

    def _queue_put(self, item):
        if type(item) is not dict:
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                self.logger.warning(f'Wrong data: {item}')
                return
        print(f'put {item}')
        self.queue.put_nowait(item)

    def _load_events(self):
        """loadEvents"""
        for event in self.event_list:
            ev = importlib.import_module(f'homedaemon.events.{event}')
            inst = ev.Event(self)
            self.events[inst.name] = inst
            self.logger.info(f'Load event: {inst.name}')

    def run(self):
        print(f'main thread {current_thread()}')
        self._load_events()
        self._listen_inputs()

        q = Thread(target=self.event_watcher, daemon=True).start()

        self.logger.info('Daemon is listening')

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.stop()
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

    def stop(self, *args, **kwargs):
        print('stop loop')
        self.loop.stop()
        for _input in self.inputs:
            print(f'sotps {_input}')
            self.inputs[_input].stop()
        for worker in self.workers:
            worker.shutdown()

    def event_watcher(self):
        """This method is """
        sleep(0.5)
        while self.loop.is_running():
            print(f'loop {current_thread()}')
            data = self.queue.get()
            event_name = data.get('cmd')
            ev = self.events.get(event_name)
            if ev:
                ev.do(data)
            else:
                self.logger.error(f'Unknown event: {data}')


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()

