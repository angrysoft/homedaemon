from homedaemon.io import BaseInput
import asyncio


class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.host = config[self.name]['ip']
        self.port = config[self.name]['port']
        self.coro = asyncio.start_server(self._handler, self.host, self.port, loop=self.loop)
        self.server = self.loop.run_until_complete(self.coro)
        addr = self.server.sockets[0].getsockname()
        print(f'Serving on {addr}')

    async def _handler(self, reader, writer):
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')
        print(f"Received from {addr}")
        self.bus.emit_cmd(data.decode())
        writer.write('ok\n'.encode())
        await writer.drain()
        writer.close()



