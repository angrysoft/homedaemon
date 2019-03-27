from aquara import GatewayWatcher
import asyncio


class Input:
    def __init__(self, queue):
        self.name = 'AquaraGateway'
        self.loop = asyncio.get_event_loop()
        gw = GatewayWatcher(queue, loop=self.loop)
        self.loop.run_until_complete(gw.listen())

    def listen(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

