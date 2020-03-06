from homedaemon.inputs import BaseInput
from bluetooth import lookup_name

class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'users'
        
        # self.yw = YeelightWatcher(self.bus.emit_cmd, loop=self.loop)