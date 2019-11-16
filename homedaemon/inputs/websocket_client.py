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
        self._conn_task = None
        self._reader_task = None
        self._send_taks = None
        self.loop.run_until_complete(self.connect())
    
    async def reader(self):
        while self.loop.is_running():
            msg = await self.websocket.recv()
            print(f'wsock cli {msg}')
            self.queue.put(msg)
    
    async def connect(self):
        while self.loop.is_running():
            try:
                self.websocket = await websockets.connect(self.uri)
                if self.websocket.open:
                    encoded = jwt.encode({'api':'1.0', 'client': 'homed'}, self.secret, algorithm='HS256')
                    await self.websocket.send(encoded.decode())
                    self._reader_task = self.loop.create_task(self.reader())
                    break
            except OSError:
                print('websock cli reconnect')
                await asyncio.sleep(5)
    
    def exception_handler(self, loop, context):
        print(f'Exception {context}')
        self.restart()
        
    def restart(self):
        try:
            self._reader_task.cancel()
            self._conn_task.cancel()
            self._send_taks.cancel()
        except AttributeError:
            pass
        del self.websocket
        self.websocket = None
        self._conn_task = self.loop.create_task(self.connect())
    
    async def send(self, msg):
        # if self.websocket and self.websocket.open:
        await self.websocket.send(msg)
        # else:
            # print('cos sie zesrało z połączniem')
            # self.restart()
            # raise ConnectionError
    
    async def stop(self):
        if self.websocket:
            await self.websocket.close()
            await self.websocket.wait_closed()
        await self.loop.close()
    
    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.stop())
     
    def __del__(self):
        if self.websocket:
            self.websocket.close()

        
class ConnectionError(Exception):
    pass

