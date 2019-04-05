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
import logging
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
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
        self.inputs_list = ['gateway', 'arduino', 'tcp', 'yeelight']
        self.event_list = ['heartbeat', 'report']
        self.queue = Queue()
        self.cli = MongoClient()
        self.db = self.cli.homedaemondb
        self.devices = self.db.devices
        self.device_data = self.db.devices_data
        self.logger = logging
        self.logger.basicConfig(filename='homed.log',
                                filemode='w',  # TODO: change to 'a' in production mode
                                format='%(asctime)s %(message)s',
                                datefmt='%m/%d/%Y %H:%M:%S')

        self.logger.info('Starting Daemon')
        self.token = None

    def watch_queue(self):
        sleep(0.5)
        while self.loop.is_running():
            q = self.queue.get()
            if q:
                self.event_watcher(q)

    async def timers(self):
        while True:
            self._queue_put({'cmd': 'timers', 'data': 'all'})
            await asyncio.sleep(60)

    def _load_inputs(self):
        for i in self.inputs_list:
            _input = importlib.import_module(f'homedaemon.inputs.{i}')
            inst = _input.Input(self._queue_put)
            self.inputs[inst.name] = inst
            self.logger.info(f'load input: {inst.name}')

    def _listen_inputs(self):
        with ThreadPoolExecutor(max_workers=len(self.inputs)) as executors:
            for _input in self.inputs:
                executors.submit(self.inputs[_input].listen, self._queue_put)

    def _queue_put(self, item):
        self.queue.put(item)
        return str(self.queue.qsize())

    def _load_events(self):
        """loadEvents"""
        for event in self.event_list:
            ev = importlib.import_module(f'homedaemon.events.{event}')
            inst = ev.Event(self)
            self.events[inst.name] = inst
            self.logger.info(f'Load event: {inst.name}')

    def run(self):
        self._load_inputs()
        self._load_events()

        q = Thread(target=self.watch_queue)
        q.setDaemon(True)
        q.start()

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
        self.loop.stop()

    def event_watcher(self, data):
        """This method is """
        if type(data) is not dict:
            return f'Wrong data: {data}'

        event_name = data.get('cmd')
        ev = self.events.get(event_name)
        if ev:
            ev.do(data)
        return 'ok\n'


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()

