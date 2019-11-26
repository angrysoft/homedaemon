
import asyncio
import jwt
from pycouchdb import Server
from aquara import GatewayWatcher
import json
import socket
import ssl

class TcpClient:
    def __init__(self, loop=None):
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
                
        db_srv = Server()
        config = db_srv.db('config')
        self.ip = config['tcp']['client']['ip']
        self.port = config['tcp']['client']['port']
        self.secret = config['tcp']['secret']
        self.loop.create_task(self.conn_watcher())
        self.reader = None
        self.writer = None
        # pem = config['tcp']['client']['pem']
        # key = config['tcp']['client']['key']
        
        self.ssl_context = ssl._create_unverified_context()
        
    async def connect(self):
        print('Connect...')
        socket.settimeout = 5
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
        # self.loop.create_task(self.msg_reader())
        
    async def conn_watcher(self, interval=5):
        while self.loop.is_running():
            if self.writer is None or self.writer.is_closing() or self.reader.at_eof():
                await self.connect()
            await asyncio.sleep(interval)
    
    async def _msg_reader(self):
        print('start msg watch')
        while not self.reader.at_eof():
            msg = await self.reader.readline()
            msg = msg.strip()
            msg = msg.decode()
            if msg:
                yield msg
                print(msg)
        print('end msg watch')
    
    def msg_reader(self):
        return self.loop.run_until_complete(self._msg_reader())
             
    async def _send(self, msg):
        if not self.writer or self.writer.is_closing():
            print('closed')
            return
        
        if type(msg) == dict:
            try:
                msg = json.dumps(msg)
            except json.JSONDecodeError as err:
                print(err)
                return
        else:
            print('Wrong data {msg}')
            return
        try:
            self.writer.write(f'{msg}\n'.encode())
            await self.writer.drain()
        except ConnectionResetError as err:
            print(err)
    
    def send(self, msg):
        self.loop.create_task(self._send(msg))
 