from yeelight import YeelightWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, bus, config):
        super(Input, self).__init__(bus)
        self.name = 'Yeelight'
        self.yw = YeelightWatcher(self.bus.emit_cmd, loop=self.loop)
