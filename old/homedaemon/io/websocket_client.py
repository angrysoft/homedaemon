import asyncio
import websockets
import sys
import jwt
import json
from homedaemon.io import BaseInput


class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
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
            try:
                msg = json.loads(msg)
            except json.JSONDecodeError as err:
                print(err)
                return
            self.bus.emit_cmd(msg)
    
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
        self.loop.create_task(self.connect())
            
     


