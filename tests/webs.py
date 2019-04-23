#!/usr/bin/python3
# WS server example that synchronizes state across clients

import asyncio
import websockets


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
                self.handler(message)
        finally:
            await self._unregister(websocket)

    async def _register(self, client):
        self.clients.add(client)

    async def _unregister(self, client):
        self.clients.remove(client)

    async def send(self, msg):
        if self.clients:
            await asyncio.wait([client.send(msg) for client in self.clients])

    def serve(self):
        self.loop.run_forever()


if __name__ == '__main__':
    ws = WebSockServer()
    ws.serve()
