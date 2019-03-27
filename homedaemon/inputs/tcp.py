import asyncio

class HomeDaemonProto:
    def __init__(self, watcher):
        self.peername = None
        self.transport = None
        self.watcher = watcher

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        ret = ''
        if data:
            _data = json.loads(data.decode())
        ret = self.watcher(_data)
        if type(ret) == str:
            self.transport.write(ret.encode())

    def eof_received(self):
        pass
        # print('wtf eof recived')

    def connection_lost(self, exc):
        # print('Lost connection of {}'.format(self.peername))
        self.transport.close()


class Input:
    def __init__(self, queue, host='127.0.0.1', port='6666'):
        self.name = 'Tcp'
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_server(lambda: HomeDaemonProto(self.queue), self.host, self.port)
        self.server = self.loop.run_until_complete(coro)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')
