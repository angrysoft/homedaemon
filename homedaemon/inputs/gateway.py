from aquara import GatewayWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__(queue)
        self.name = 'AquaraGateway'
        gw = GatewayWatcher(queue, loop=self.loop)
        self.loop.run_until_complete(gw.listen())

