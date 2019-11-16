import asyncio
import websockets
import sys
import jwt
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'websocket_client'
        url = config['websocket']['webserver']['ip']
        port = config['websocket']['webserver']['port']
        self.secret = config['websocket']['secret']
        self.urltoken = config['websocket']['urltoken']
        self.websocket = None
        if config['websocket']['webserver']['ssl']:
            proto = 'wss'
        else:
            proto = 'ws'
        self.uri = f'{proto}://{url}:{port}?token={self.urltoken}'
        self.loop.set_exception_handler(self.exception_handler)
        
    
    async def reader(self):
        while self.loop.is_running():
            msg = await self.websocket.recv()
            self.queue.put(msg)
    
    async def connect(self):
        while self.loop.is_running():
            if self.websocket and self.websocket.open:
                await asyncio.sleep(5)
                continue
            try:
                print('websock cli connecting..')
                self.websocket = await websockets.connect(self.uri)
                if self.websocket.open:
                    encoded = jwt.encode({'api':'1.0', 'client': 'homed'}, self.secret, algorithm='HS256')
                    await self.websocket.send(encoded.decode())
                    self.loop.create_task(self.reader())
            except OSError:
                await asyncio.sleep(3)
    
    def exception_handler(self, loop, context):
        print(f'Exception {context}')
        self.loop.create_task(self.websocket.close())
    
    async def send(self, msg):
        await self.websocket.send(msg)
    
    def run(self):
        try:
            self.loop.create_task(self.connect())
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()
            self.loop.run_until_complete(self.websocket.close())
            self.loop.run_until_complete(self.websocket.wait_closed())
     


