import asyncio
import websockets
import sys
import jwt
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'websocket_client'
        self.url = config['websocket']['webserver']['ip']
        self.port = config['websocket']['webserver']['port']
        self.secret = config['websocket']['secret']
        self.urltoken = config['websocket']['urltoken']
        self.websocket = None
        if config['websocket']['webserver']['ssl']:
            proto = 'wss'
        else:
            proto = 'ws'
        self.uri = f'{proto}://{url}:{port}?token={self.urltoken}'
        self.loop.set_exception_handler(self.exception_handler)
        self._conn_task = None
        self._reader_task = None
        self._send_taks = None
    
    async def reader(self):
        while self.loop.is_running():
            msg = await self.websocket.recv()
            self.queue.put(msg)
    
    async def connect(self):
        while True:
            try:
                self.websocket = await websockets.connect(self.uri)
                if self.websocket.open:
                    encoded = jwt.encode({'api':'1.0', 'client': 'homed'}, self.secret, algorithm='HS256')
                    print(encoded.decode())
                    await self.websocket.send(encoded.decode())
                    self._reader_task = self.loop.create_task(self.reader())
                    break
            except OSError:
                print('try reconnect in 5 sec')
                await asyncio.sleep(5)
    
    def exception_handler(self, loop, context):
        print(f'exception from input :{context}')
        try:
            self._reader_task.cancel()
            self._conn_task.cancel()
            self._send_taks.cancel()
        except AttributeError:
            pass
        del self.websocket
        self.websocket = None
        self._conn_task = self.loop.create_task(self.connect())
    
    def send(self, msg):
        if self.websocket and self.websocket.open:
            self._send_taks = self.loop.create_task(self._send(msg))
        else:
            raise ConnectionError
    
    async def _send(self, msg):
        await self.websocket.send(msg)
    
    async def stop(self):
        if self.websocket:
            await self.websocket.close()
     
    def __del__(self):
        if self.websocket:
            self.websocket.close()

    # async def send(self, msg):
    #     if self.clients:
    #         await asyncio.wait([client.send(msg) for client in self.clients])


class ConnectionError(Exception):
    pass

