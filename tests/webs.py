#!/usr/bin/python3
# WS server example that synchronizes state across clients

import asyncio
import websockets
import json


class WebSockServer:
    def __init__(self, handeler=print, url='127.0.0.1', port=9000, loop=None):
        self.url = url
        self.port = port
        self.handler = handeler
        self.clients = set()
        self.loop = loop
        if self.loop is None:
            try:
                self.loop = asyncio.get_event_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(websockets.serve(self._handler, self.url, self.port))

    async def _handler(self, websocket, path):
        await self._register(websocket)
        try:
            async for message in websocket:
                self.handler(message, self)
        finally:
            await self._unregister(websocket)

    async def _register(self, client):
        self.clients.add(client)

    async def _unregister(self, client):
        self.clients.remove(client)

    def send(self, msg):
        if self.clients:
            print(f'sending {msg}')
            self.loop.create_task(self._send(msg))

    async def _send(self, msg):
        await asyncio.wait([client.send(msg) for client in self.clients])

    def serve(self):
        self.loop.run_forever()


async def sender(ws):
    while True:
        await ws.send('dupa')
        await asyncio.sleep(2)


def echo(msg, sock):
    data = json.loads(msg)
    data['cmd'] = 'report'
    sock.send(json.dumps(data))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    ws = WebSockServer(echo, loop=loop)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()


