from . import BaseDevice
from yeelight import Bulb


class YeeligthDevice(BaseDevice):
    def __init__(self, data, daemon):
        super(YeeligthDevice, self).__init__(data, daemon)
        self.support = data.get('support')
        self.ip = data.get('ip')

    def write(self, data):
        _data = data.get('data')
        c, v = _data.popitem()
        if c in self.support:
            return self._send(c, v)

    def _send(self, c, v):
        bulb = Bulb(self.ip)
        ret = None
        if c == 'set_power':
            if type(v) is str:
                ret = bulb.set_power(v)
            elif type(v) is dict:
                ret = bulb.set_power(v.get('power'),
                                     efx=v.get('efx', 'smooth'),
                                     duration=v.get('duration', 500),
                                     mode=v.get('mode', 0))
                
        elif c == 'toogle':
            ret = bulb.toggle()
        elif c == 'set_ct' and v is dict and 'ct' in v:
            ret = bulb.set_ct_abx(v['ct'],
                                  efx=v.get('efx', 'smooth'),
                                  duration=v.get('duration', 500))
        elif c == 'set_bright' and v is dict and 'bright' in v:
            ret = bulb.set_bright(v['bright'],
                                  efx=v.get('efx', 'smooth'),
                                  duration=v.get('duration', 500))
        elif c == 'set_default':
            ret = bulb.set_default()
        elif c == 'start_cf' and v is dict:
            ret = bulb.start_cf(count=v.get('count', 0),
                                action=v.get('action', 0),
                                flow_expression=v.get('flow_expression',
                                                      '1000, 2, 2700, 100, 500, 1'))
        elif c == 'stop_cf':
            ret = bulb.stop_cf()
        elif c == 'set_scene' and v is dict and {'scene_class', 'args'}.issubset(v):
            ret = bulb.set_scene(v['scene_class'], v['args'])
        return ret
