
import asyncio
import jwt
from pycouchdb import Server
import json
import socket
import ssl

class TcpClient:
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
         
        db_srv = Server()
        config = db_srv.db('config')
        self.ip = config['tcp']['client']['ip']
        self.port = config['tcp']['client']['port']
        self.secret = config['tcp']['secret']
        self.queue = Queue()
        self.loop.create_task(self.conn_watcher())
        self.loop.create_task(self.msg_reader())
        self.reader = None
        self.writer = None
        self.ssl_context = ssl.create_default_context()
        # self.ssl_context = ssl._create_unverified_context()
    
    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()

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
        encoded = jwt.encode({'api':'1.0', 'client': 'www'}, self.secret, algorithm='HS256')
        self.writer.write(encoded + '\n'.encode())
        await self.writer.drain()
        self.loop.create_task(self.msg_reader())
        
    async def conn_watcher(self, interval=5):
        while self.loop.is_running():
            if not self.is_connected():
                await self.connect()
            await asyncio.sleep(interval)
    
    async def msg_reader(self):
        while self.reader and not self.reader.at_eof():
            msg = await self.reader.readline()
            msg = msg.strip()
            print(f'{msg}')
            self.queue.put(msg.decode())
             
    async def _send(self, msg):
        if not self.is_connected():
            print('closed')
            return
        
        if type(msg) == dict:
            try:
                msg = json.dumps(msg)
            except json.JSONDecodeError as err:
                print(err)
                return
            
        self.writer.write(f'{msg}\n'.encode())
        await self.writer.drain()
    
    def send(self, msg):
        self.loop.create_task(self._send(msg))
    
    def is_connected(self):
        if self.writer is None or self.writer.is_closing() or self.reader.at_eof():
            return False
        else:
            return True

class Queue:
    def __init__(self):
        self._queue = None
        self.lock = asyncio.Lock()

    def put(self, item):
        self._queue = item

    def get(self):
        if self._queue:
                msg = self._queue
                self._queue = None
                return msg
        else:
            return None

    def not_empty(self):
        if self._queue:
            return True
        else:
            return False
    
 
if __name__ == "__main__":
    t = TcpClient()
    t.run()
     