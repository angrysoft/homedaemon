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
import sys
import logging
from threading import Thread, current_thread, RLock
from time import sleep
from pycouchdb import Server
from systemd.journal import JournalHandler
from homedaemon.devices import Device

logger = logging.getLogger('homed')
logger.addHandler(JournalHandler())
logger.setLevel(logging.DEBUG)


class HomeDaemon:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.inputs = dict()
        self.inputs_list = [
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
        self.logger = logger
        self.logger.info('Starting Daemon')
        self.token = None
        self.workers = dict()
        self.scenes = dict()
        self.triggers = Triggers()

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
            self.workers[dev['sid']] = Device(dev, self)

    def _load_scenes(self):
        sys.path.append(self.config['scenes']['path'])
        scene_list = list()
        with os.scandir(self.config['scenes']['path']) as it:
            for entry in it:
                if entry.name.endswith('.py') and entry.is_file():
                    _scene = importlib.import_module(entry.name[:-3])
                    inst = _scene.Scene(self)
                    self.scenes[inst.name] = inst
                    Trigger(inst.trigger, inst)
                    print(f'loaded {inst.name}')
                    scene_list.append({'name': inst.name, 'automaitc': inst.automatic })
            self.config['scenes_list'] = {'list':scene_list}


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
            sid = data.get('sid')
            if sid in self.workers:
                try:
                    self.workers[sid].do(data)
                except ValueError as err:
                    self.logger.error(f'{sid} {err}')
            elif sid in self.scenes:
                try:
                    self.scenes[sid].do(data.get('data', {}))
                except ValueError as err:
                    self.loop.error(f'{sid} {err}')
            else:
                self.logger.error(f'Unknown sid: {data}')
        self.logger.info('Stop watching')

class Queue:
    def __init__(self):
        self._queue = list()
        self.lock = RLock()

    def put(self, item):
        with self.lock:
            if type(item) is not dict:
                try:
                    item = json.loads(item)
                except json.JSONDecodeError:
                    logger.warning(f'Wrong data: {item}')
                    return
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


class Triggers:
    def __init__(self):
        self._triggers = dict()
    
    def register(self, trigger):
        if trigger is not isinstance(Trigger):
            raise ValueError('arg need to by Trigger instance')
        if trigger.sid not in self._triggers:
            self._triggers[trigger.sid] = list()

        self._triggers[trigger.sid].append(trigger)

    def unregister(self, ):
        pass

    def on_event(self, event):
        try:
            name , value = event.get('data').popitem()
        except KeyError:
            return

        for trigger in self._triggers.get(event.get('sid'), []):
            if trigger.event == name and trigger.value == value:
                trigger.pull()
            

class Trigger:
    def __init__(self, trigger, scene):
        if type(trigger) is str:
            _values = trigger.split('.')
            if len(_values) == 3:
                self.sid, self.event, self.value = _values
                print(self.sid, self.event, self.value)
        self._scene = scene
    
    def pull(self):
        self._scene.do({'status', 'on'})
        


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()
