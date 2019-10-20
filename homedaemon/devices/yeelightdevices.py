from . import BaseDevice, ButtonOnOff
from yeelight import Bulb


class YeeligthDevice(BaseDevice):
    def __init__(self, data, daemon):
        super(YeeligthDevice, self).__init__(data, daemon)
        self.support = data.get('support')
        self.ip = data.get('ip')
        self.bulb = Bulb(data.get('ip'))
        self.power = ButtonOnOff('set_power', self.write)

    def write(self, data):
        print(data)
        _data = data.get('data')
        if _data is None:
            self.daemon.logger.error('Yeelight write :data is empty')
            return
        c, v = _data.popitem()
        self._send(c, v)
        {'set_power': self.set_power,
         'on', self.}
    
    def on(self):
        self.bulb.set_power('on')

    def off(self):
        self.bulb.set_power('off')

    def toggle(self):
        self.bulb.toggle()

    def bright(self, value):
        self.bulb.set_bright(int(value))
    
    def set_rgb(self, r, g, b):
        self.bulb.set_rgb(r, g, b)

    def set_default(self):
        self.bulb.set_default()
    
    def set_ct_abx(self, value):
        self.bulb.set_ct_abx(int(value))

    def _send(self, c, v):
        # bulb = Bulb(self.ip)
        if c == 'set_power':
            if type(v) is str:
                self.bulb.set_power(v)
            elif type(v) is dict:
                self.bulb.set_power(v.get('power'),
                                    efx=v.get('efx', 'smooth'),
                                    duration=v.get('duration', 500),
                                    mode=v.get('mode', 0))
                
        elif c == 'toogle':
            self.bulb.toggle()
        
        elif c == 'set_rgb':
            self.bulb.set_rgb(v['red'], v['green'], v['blue'])
        
        elif c == 'set_ct':
             if type(v) is dict:
                self.bulb.set_ct_abx(int(v['set_ct']),
                                     efx=v.get('efx', 'smooth'),
                                     duration=v.get('duration', 500))
             else:
                self.bulb.set_ct_abx(int(v))

        elif c == 'set_bright':
            if type(v) is dict:
                self.bulb.set_bright(int(v['set_bright']),
                                     efx=v.get('efx', 'smooth'),
                                     duration=v.get('duration', 500))
            else:
                self.bulb.set_bright(int(v))
                
        elif c == 'set_default':
            self.bulb.set_default()
        elif c == 'start_cf' and v is dict:
            self.bulb.start_cf(count=v.get('count', 0),
                               action=v.get('action', 0),
                               flow_expression=v.get('flow_expression',
                                                     '1000, 2, 2700, 100, 500, 1'))
        elif c == 'stop_cf':
            self.bulb.stop_cf()
        elif c == 'set_scene' and v is dict and {'scene_class', 'args'}.issubset(v):
            self.bulb.set_scene(v['scene_class'], v['args'])
