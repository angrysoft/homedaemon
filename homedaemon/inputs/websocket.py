import asyncio
import websockets
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, handler=print, url='127.0.0.1', port=9000):
        super(Input, self).__init__()
        self.name = 'websocket'
        self.url = url
        self.port = port
        self.handler = handler
        self.clients = set()
        self.server = self.loop.run_until_complete(websockets.serve(self._handler, self.url, self.port))

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

    def send(self, msg):
        print(f'prare sending {len(self.clients)}')
        if self.clients:
            # await asyncio.wait([client.send(msg) for client in self.clients])
            self.loop.create_task(self._send(msg))

    async def _send(self, msg):
        print(f'_sending {msg}')
        for client in self.clients:
            await client.send(msg)

    def quit(self):
        self.loop.stop()
        self.server.close()
