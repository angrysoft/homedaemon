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
        self.loop = None
        self.host = host
        self.port = port
        self.buffer_size = 1024

    async def run(self):
        self.server = await asyncio.start_server(self.event_watcher,
                                                 self.host,
                                                 self.port)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        self.loop = self.server.get_loop()
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.run_until_complete(self.server.wait_closed())
        async with self.server:
            await self.server.serve_forever()

    async def event_watcher(self, reader, writer):
        """This method is """
        data = await reader.read(self.buffer_size)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")

    def stop(self):
        self.server.close()
        self.loop.stop()


if __name__ == '__main__':
    hd = HomeDaemon()
    asyncio.run(hd.run())

