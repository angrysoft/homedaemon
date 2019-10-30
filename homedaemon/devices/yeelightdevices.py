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
        
        {'set_power': self.set_power,
         'set_rgb': self.set_rgb,
         'set_ct_abx': self.set_ct_abx,
         'set_bright': self.bright}.get(c, self.unknown)(v)
    
    def unknown(self, value):
        self.daemon.logger.erro(f'unknown parametr {value}')
    
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

    def set_default(self, *args):
        self.bulb.set_default()
    
    def set_ct_abx(self, value):
        self.bulb.set_ct_abx(int(value))
    
    def set_power(self, value):
        if type(value) is str:
            self.bulb.set_power(value)
        elif type(value) is dict:
            self.bulb.set_power(value.get('power'),
                                efx=value.get('efx', 'smooth'),
                                duration=value.get('duration', 500),
                                mode=value.get('mode', 0))

    def set_scene(self, value):
        if value is dict and {'scene_class', 'args'}.issubset(value):
            self.bulb.set_scene(value['scene_class'], value['args'])
