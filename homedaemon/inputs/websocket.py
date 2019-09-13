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
        self.loop.set_exception_handler(self.exception_handler)
        self.start_server()

    def restart_server(self):
        print('restarting server')
        self.loop.stop()
        self.clients.clear()
        self.start_server()

    def start_server(self):
        self.server = self.loop.run_until_complete(websockets.serve(self._handler, self.url, self.port))

    def exception_handler(self, loop, context):
        loop.stop()
        self.clients.clear()
        print(f'exception from input :{context}')
        self.start_server()

    async def _handler(self, _websocket, path):
        await self._register(_websocket)
        try:
            async for message in _websocket:
                await self.queue.put(message)
        except websockets.exceptions.ConnectionClosed:
            self.restart_server()
        finally:
            await self._unregister(_websocket)

    async def _register(self, client):
        self.clients.add(client)

    async def _unregister(self, client):
        self.clients.remove(client)

    async def send(self, msg):
        if self.clients:
            await asyncio.wait([client.send(msg) for client in self.clients])


