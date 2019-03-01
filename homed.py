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
import sys
sys.path.append('/etc/smarthouse')


class HomeDaemonProto:
    def __init__(self, watcher):
        self.peername = None
        self.transport = None
        self.watcher = watcher

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        ret = self.watcher(data)
        if type(ret) == str:
            self.transport.write(ret.encode())

    def eof_received(self):
        print('wtf eof recived')

    def connection_lost(self, exc):
        print('Lost connection of {}'.format(self.peername))
        self.transport.close()


class HomeDaemon:
    def __init__(self, host='127.0.0.1', port=6666):
        self.server = None
        self.loop = asyncio.get_event_loop()
        self.host = host
        self.port = port
        self.buffer_size = 1024
        self.transport = None
        self.protocol = None
        self.peername = ''

    def run(self):
        coro = self.loop.create_server(lambda: HomeDaemonProto(self.event_watcher), self.host, self.port)
        self.server = self.loop.run_until_complete(coro)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.stop()
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGHUP, self.stop)
        self.loop.add_signal_handler(signal.SIGQUIT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        self.loop.run_forever()

    def stop(self, *args, **kwargs):
        # self.loop.stop()
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.stop()

    def event_watcher(self, data):
        """This method is """
        print(f'Data {data}')
        return 'ok\n'


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()

