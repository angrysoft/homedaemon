import asyncio
import websockets
import sys
import ssl
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'websocket'
        self.url = config['websocket']['ip']
        self.port = config['websocket']['port']
        self.ssl = config['websocket']['ssl']
        self.pemfile = config['websocket']['pem']
        self.keyfile = config['websocket']['key']
        self.clients = set()
        self.server = None
        self.srv = None
        self.loop.set_exception_handler(self.exception_handler)
        self.start_server()

    def restart_server(self):
        print('Restarting server')
        self.loop.stop()
        self.clients.clear()
        del self.server
        self.server = None
        self.start_server()


    def start_server(self):
        print('Starting websocket server')
        if self.ssl:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.pemfile, self.keyfile)
            self.server = websockets.serve(self._handler, self.url, self.port, ssl=context)
        else:
            self.server = websockets.serve(self._handler, self.url, self.port)
        self.srv = self.loop.run_until_complete(self.server)

    def exception_handler(self, loop, context):
        print(f'exception from input :{context}')
        self.restart_server()

    async def _handler(self, _websocket, path):
        await self._register(_websocket)
        try:
            async for message in _websocket:
                self.queue.put(message)
        finally:
            await self._unregister(_websocket)

    async def _register(self, client):
        self.clients.add(client)

    async def _unregister(self, client):
        self.clients.discard(client)
        await client.close()

    async def send(self, msg):
        if self.clients:
            await asyncio.wait([client.send(msg) for client in self.clients])


