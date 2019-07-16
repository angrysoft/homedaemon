import asyncio
import websockets
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'websocket'
        self.url = config['websocket']['ip']
        self.port = config['websocket']['port']
        self.clients = set()
        self.server = None
        self.start_server()

    def start_server(self):
        self.loop.set_exception_handler(self.exception_handler)
        self.server = self.loop.run_until_complete(websockets.serve(self._handler, self.url, self.port))

    def exception_handler(self, loop, context):
        loop.stop()
        self.clients.clear()
        print(f'exception from input :{context}')
        self.start_server()

    async def _handler(self, websocket, path):
        await self._register(websocket)
        try:
            async for message in websocket:
                self.queue.put(message)
        finally:
            await self._unregister(websocket)

    async def _register(self, client):
        self.clients.add(client)

    async def _unregister(self, client):
        self.clients.remove(client)

    async def send(self, msg):
        if self.clients:
            await asyncio.wait([client.send(msg) for client in self.clients])


