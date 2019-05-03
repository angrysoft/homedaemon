from homedaemon.inputs import BaseInput
import asyncio


class Input(BaseInput):
    def __init__(self, queue, host='127.0.0.1', port='6666'):
        super(Input, self).__init__()
        self.name = 'Tcp'
        self.host = host
        self.port = port
        self.queue = queue
        self.coro = asyncio.start_server(self._handler, self.host, self.port, loop=self.loop)
        self.server = self.loop.run_until_complete(self.coro)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')

    async def _handler(self, reader, writer):
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')
        print(f"Received from {addr}")
        self.queue(data.decode())
        writer.write('ok\n'.encode())
        await writer.drain()
        writer.close()

    def stop(self):
        self.loop.stop()
        self.server.close()

        self.loop.create_task(self.server.wait_closed())
        # self.loop.close()
        print('tcp stops')


