import json
from homedaemon.inputs import BaseInput


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
        self.watcher(data)
        self.transport.write('ok\n'.encode())

    def eof_received(self):
        pass
        # print('wtf eof recived')

    def connection_lost(self, exc):
        # print('Lost connection of {}'.format(self.peername))
        self.transport.close()


class Input(BaseInput):
    def __init__(self, queue, host='127.0.0.1', port='6666'):
        super(Input, self).__init__()
        self.name = 'Tcp'
        self.host = host
        self.port = port
        coro = self.loop.create_server(lambda: HomeDaemonProto(queue), self.host, self.port)
        self.server = self.loop.run_until_complete(coro)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')

