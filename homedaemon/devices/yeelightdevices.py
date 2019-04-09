from . import BaseDevice
from yeelight import Bulb


class YeeligthDevice(BaseDevice):
    def __init__(self, data):
        super(YeeligthDevice, self).__init__(data)
        self.support = data.get('support')
        self.ip  = data.get('ip')

    def do(self, **kwargs):
        if 'cmd' not in kwargs:
            return
        cmd = kwargs['cmd']

        for c,v in cmd:
            if c in self.support:
                self._send(c, v)

    def _send(self, c, v):
        bulb = Bulb(self.ip)
        if c == 'on':
            bulb.on()
        elif c == 'off':
            bulb.off()
        elif c == 'toogle':
            bulb.toggle()
        elif c == 'set_power':
            bulb.set_power(v)
