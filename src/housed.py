#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# housed.py
# Copyright (C) 2014-2018  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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
__copyright__ = 'Copyright 2014 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.5'

import socket
import os
from time import sleep
import serial
import signal
import asyncio
import argparse
import importlib
from shutil import chown


class Queue:
    """Queue fifo list"""
    def __init__(self):
        self.q = []

    def put(self, arg):
        """put arg on end of list"""
        self.q.insert(0, arg)

    def pop(self):
        """pop"""
        return self.q.pop()

    def len(self):
        """len return size of queue"""
        return len(self.q)

    def notEmpty(self):
        """notEmpty"""
        if len(self.q) > 0:
            return True
        else:
            return False


class HouseDeamon:
    """Class eventListner"""
    def __init__(self, config):
        """Constructor for eventListner"""
        self.loop = asyncio.get_event_loop()
        self.socketFile = config.socket
        self.serialPort = config.port
        self.controller = serial.Serial()
        self.controller.baudrate = 9600
        self.controller.port = self.serialPort
        self.controller.timeout = 0
        self.status = dict()
        self.events = dict()

    def _connectSerial(self):
        """docstring for __connect"""
        while True:
            if os.path.exists(self.serialPort):
                self.controller.open()
                if self.controller.readable():
                    print('Serial is redable')
                if self.controller.writable():
                    print('Serial is writable')
                self.status['connection'] = 'Connected'
                print('connectetd serial')
                self.loop.add_reader(self.controller, self.getSerialEvent)
                break
            sleep(3)

    def _diconnectSerial(self):
        """_diconnectSerial"""
        self.loop.remove_reader(self.controller)
        self.controller.close()

    def _connectSocket(self):
        """_connectSocket"""
        if os.path.exists(self.socketFile):
            os.unlink(self.socketFile)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(self.socketFile)
        chown(self.socketFile, group='uwsgi'
                                     '')
        os.chmod(self.socketFile, 664)
        self.loop.add_reader(self.sock, self.getSocketEvent)

    def _disconnectSocket(self):
        """_disconnectSocket"""
        self.loop.remove_reader(self.sock)
        self.sock.close()
        if os.path.exists(self.socketFile):
            os.unlink(self.socketFile)

    def _signals(self):
        """_signals"""
        self.loop.add_signal_handler(signal.SIGINT, self.stopLoop)
        self.loop.add_signal_handler(signal.SIGHUP, self.stopLoop)
        self.loop.add_signal_handler(signal.SIGQUIT, self.stopLoop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stopLoop)

    def _setup(self):
        """_setup"""
        # Socket listener
        self._connectSocket()
        # Serial listener
        self._connectSerial()
        # add Signals handle
        self._signals()  # TODO: do poprawki coś się jebie
        # Load events
        self._loadEvents()

    def getSocketEvent(self):
        """getSocketEvent"""
        try:
            data = self.sock.recv(1024)
            if data:
                data = data.decode('utf-8')
                if data == 'quit':
                    self.stopLoop()
                    return
                print("debug getSocketEv: ", data)  # TODO: remove
                self.emitEvent(data)
        except:
            pass

    def getSerialEvent(self):
        """getSerialEvent"""
        try:
            b = self.controller.read().decode()
            data = ''
            while not b == '\n':
                data += b
                b = self.controller.read().decode()
            print("debug getSerialEv: ", data)  # TODO: remove
        except:
            return

    def _loadEvents(self):
        """loadEvents"""
        eventList = list()
        for e in os.listdir('events'):
            if e.endswith('.py') and not e.startswith('__'):
                if e == 'event.py':
                    continue
                e = '.' + e.replace('.py', '')
                eventList.append(e)

        importlib.import_module('events')

        for event in eventList:
            ev = importlib.import_module(event, package="events")
            inst = ev.Event()
            self.events[inst.name] = inst
            print('Load event: {0}'.format(inst.name))

    def emitEvent(self, e):
        """doEvent"""
        eventName, eventValue = e.split(':', 1)
        ev = self.events.get(eventName)
        if ev:
            ev.run(self.controller, args=eventValue)

    def watchEmiter(self):
        """watchEmiter"""
        self._setup()
        self.loop.run_forever()

    def stopLoop(self, *args):
        """stop"""
        self._diconnectSerial()
        self._disconnectSocket()
        self.loop.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='%(prog)s [options] [packagees]')
    parser.add_argument('-p', '--port', default='/dev/ttyACM0',  help='Serial port')
    parser.add_argument('-s', '--socket', default='/tmp/housed.sock',  help='Socket file')
    d = HouseDeamon(parser.parse_args())
    d.watchEmiter()
