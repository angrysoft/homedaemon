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
        # coro = asyncio.start_server(self.event_watcher,
        #                             self.host,
        #                             self.port,
        #                             loop=self.loop)
        coro = self.loop.create_server(self, self.host, self.port)
        self.server = self.loop.run_until_complete(coro)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.stop()

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        # self.transport.write('ok\n')

    def connection_lost(self, exc):
        print('Lost connection of {}'.format(self.peername))
        self.transport.close()

    async def event_watcher(self, reader, writer):
        """This method is """
        data = await reader.readline()
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")


if __name__ == '__main__':
    hd = HomeDaemon()
    hd.run()

