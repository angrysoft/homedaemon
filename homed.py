#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# homed.py
# Copyright (C) 2014-2021  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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
__copyright__ = 'Copyright 2014-2021 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.9.5'


import asyncio
from homedaemon.io import BaseInput
import importlib
from threading import current_thread
from typing import Dict
from homedaemon.devices import DevicesManager
from homedaemon.bus import Bus
from homedaemon.logger import Logger
from homedaemon.config import JsonConfig, ArgConfig, Config, ConfigError
import argparse


class HomeDaemon:
    def __init__(self, config: Config) -> None:
        self.config = config
        if not self.config.get("homed", {}).get('homeid'):
            raise ConfigError('Missing config value homed -> homeid')
        
        self.logger = Logger(debug=args.debug, std=args.log_to_stdout)
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
        self.inputs: Dict[str, BaseInput] = dict()
        self.bus = Bus(self.loop)
        self.logger.info('Starting Daemon')
        self.devices_manager = DevicesManager()
        self.bus.add_trigger('*.*.*.*', self.logger.debug)

    def load_inputs(self) -> None:
        _input_name : str
        for _input_name in self.config['io']:
            self.loop.run_in_executor(None, self._input, _input_name)
            
    def _input(self, _input_name:str) -> None:
        _input = importlib.import_module(f'homedaemon.io.{_input_name}')
        inst: BaseInput = _input.Input(self.bus, self.config, self.loop)
        inst.name = _input_name
        self.inputs[inst.name] = inst
        self.logger.info(f'load input: {inst.name}')
        self.inputs[inst.name].run()

        
    def run(self) -> None:
        self.logger.debug(f'main thread {current_thread()} loop {id(self.loop)}')
        # self.loop.run_in_executor(None, self.load_inputs)
        # self.loop.run_in_executor(None, self.load_devices)
        self.load_inputs()
        self.devices_manager.register_devices()
        # self.loop.add_signal_handler(signal.SIGINT, self.stop)
        # self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        # self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        # self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        # return
        try:
            self.bus.emit('info.homed.status.started', {"msg": "HomeDaemon started"})
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()
        # finally:
        #     try:
                
        #         self._cancel_all_tasks()
        #         self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        #     finally:
        #         self.loop.close()

    # def stop(self, *args, **kwargs):
    #     self.logger.info('Stop homed')
    #     try:
    #         self.loop.stop()
    #         self._cancel_all_tasks()
    #         self.loop.run_until_complete(self.loop.shutdown_asyncgens())
    #     finally:
    #         self.loop.close()
    
    def _cancel_all_tasks(self) -> None:
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
    parser.add_argument('-D', '--debug', action="store_true", help="Debug msg")
    parser.add_argument('-d', '--devices-dir', nargs='?', default='/etc/homedaemon/dev.d', help='Path to devices dir')
    parser.add_argument('-s', '--log-to-stdout', action="store_true", help="Print log info to stdout")
    parser.add_argument('-c', '--config-dir', nargs='?', default='/etc/homedaemon/conf.d', help='Path to config dir')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    
    config: Config = Config()
    config.load_config(JsonConfig(args.config_dir))
    config.load_config(ArgConfig(args))
    hd = HomeDaemon(config)
    hd.run()
   
