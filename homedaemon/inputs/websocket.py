import asyncio
import websockets
import sys
import ssl
import jwt
from homedaemon.inputs import BaseInput
from urllib.parse import urlparse, parse_qs


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'websocket'
        self.url = config['websocket']['ip']
        self.port = config['websocket']['port']
        self.ssl = config['websocket']['ssl']
        self.secret = config['websocket']['secret']
        pemfile = config['websocket']['pem']
        keyfile = config['websocket']['key']
        self.urltoken = config['websocket']['urltoken']
        self.clients = set()
        self.server = None
        self.srv = None
        if 'pem' in self.config and 'key' in self.config:
            pemfile = self.config['pem']
            keyfile = self.config['key']
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(pemfile, keyfile)
            server = websockets.serve(self._handler, self.url, self.port, ssl=context)
        else:
            server = websockets.serve(self._handler, self.url, self.port)
        self.loop.run_until_complete(server)

    # def restart_server(self):
    #     print('Restarting server')
    #     self.loop.stop()
    #     self.clients.clear()
    #     del self.server
    #     self.server = None
    #     self.start_server()


    # def start_server(self):
    #     print('Starting websocket server')
    #     if self.ssl:
    #         context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #         context.load_cert_chain(self.pemfile, self.keyfile)
    #         self.server = websockets.serve(self._handler, self.url, self.port, ssl=context)
    #     else:
    #         self.server = websockets.serve(self._handler, self.url, self.port)
    #     self.srv = self.loop.run_until_complete(self.server)

    def exception_handler(self, loop, context):
        print(f'exception from input :{context}')
        self.restart_server()

    async def _handler(self, websocket, path):
        if not self._connect_token_check(path):
            await websocket.close()
            print(f'closing connection for {websocket.host}')
            return
        try:
            async for message in websocket:
                await self.msg_handler(message, websocket)
        finally:
            await self._unregister(websocket)
    
    async def msg_handler(self, msg, wsock) -> None:
        _id = id(wsock)
        if _id not in self.clients:
            await self._register(wsock, msg)
            return
            
        self.queue.put(msg)
    
    def _connect_token_check(self, path):
        args = urlparse(path)
        token = parse_qs(args.query).get('token', [''])[0]
        if token == self.urltoken:
            return True
        else:
            return False

    async def _register(self, client, token):
        try:
            decoded = jwt.decode(token, self.secret, algorithms='HS256')
        except jwt.InvalidSignatureError as err:
            print(err)
        except jwt.DecodeError as err:
            print(err)
        except jwt.InvalidTokenError as err:
            print(err)
        else:
            self.clients.add(client)
            return
        print('not registred')
        await client.close()

    async def _unregister(self, client):
        await client.close()
        try:
            self.clients.discard(client)
        except KeyError:
            pass

    async def send(self, msg):
        if self.clients:
            await asyncio.wait([self.clients[client].send(msg) for client in self.clients])


