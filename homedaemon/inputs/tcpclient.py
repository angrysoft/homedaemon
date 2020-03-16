from homedaemon.inputs import BaseInput
import asyncio
import ssl
import socket
import jwt
import json

class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'tcpclient'
        self.ip = config['tcp']['client']['ip']
        self.port = config['tcp']['client']['port']
        self.secret = config['tcp']['secret']
        self.ssl_context = ssl.create_default_context()
        self.reader = None
        self.writer = None
        self.loop.create_task(self.conn_watcher())
        self.bus.on('report', '*', self.send)
        self.bus.on('scene', '*', self.send)
        # self.ssl_context = ssl._create_unverified_context()

    async def connect(self):
        print('Connect...')
        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip,
                                                                     self.port, ssl=self.ssl_context)
            
        except ConnectionRefusedError as err:
            print(err)
            return
        except OSError as err:
            print(err)
            return
        encoded = jwt.encode({'api':'1.0', 'client': 'homed'}, self.secret, algorithm='HS256')
        self.writer.write(encoded + '\n'.encode())
        await self.writer.drain()
        self.loop.create_task(self.msg_reader())
        if self.is_connected():
            self.bus.emit_cmd({'cmd': 'connected', 'sid': self.name, 'data':{}})
        
    async def conn_watcher(self, interval=5):
        while self.loop.is_running():
            if not self.is_connected():
                await self.connect()
            await asyncio.sleep(interval)
    
    async def msg_reader(self):
        while self.reader and not self.reader.at_eof():
            msg = await self.reader.readline()
            msg = msg.strip()
            try:
                msg = json.loads(msg)
            except json.JSONDecodeError as err:
                print(err)
                return
            self.bus.emit_cmd(msg)
             
    async def send(self, msg):
        if not self.is_connected():
            print('closed')
            return
        
        if type(msg) == dict:
            try:
                msg = json.dumps(msg)
            except json.JSONDecodeError as err:
                print(err)
                return
        try:    
            self.writer.write(f'{msg}\n'.encode())
            await self.writer.drain()
        except ConnectionRefusedError as err:
            self.writer = None
    
    def is_connected(self):
        if self.writer is None or self.writer.is_closing() or self.reader.at_eof():
            return False
        else:
            return True
        