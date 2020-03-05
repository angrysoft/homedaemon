from pyxiaomi import GatewayWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'AquaraGateway'
        self.gw = GatewayWatcher(self.bus.emit_cmd, loop=self.loop)
        self.loop.create_task(self.gw.listen())


