from .base import BaseDevice, ButtonOnOff, Dummy
from pyxiaomi import DeskLamp, Bslamp1, Color, YeelightDev
import asyncio

class YeeligthDevice:
    def __new__(cls, data, daemon):
        return {'color': ColorDev,
                'bslamp1': Bslamp1Dev,
                'desklamp': DeskLampDev}.get(data.get('model'), Dummy)(data, daemon)


class White(BaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.support = data.get('support')
        self.ip = data.get('ip')
        self.dev = YeelightDev(ip='auto', sid=self.sid)
        self.power = ButtonOnOff('set_power', self.write)
        self.cmd = {'set_power': self.set_power,
                    'set_ct_abx': self.set_ct_abx,
                    'set_bright': self.bright}

    def write(self, data):
        print(data)
        _data = data.get('data')
        if _data is None:
            self.daemon.logger.error('Yeelight write :data is empty')
            return
        c, v = _data.popitem()
        
        self.cmd.get(c, self.unknown)(v)
    
    def unknown(self, value):
        self.daemon.logger.error(f'unknown parametr {value}')
    
    def on(self):
        self.dev.set_power('on')

    def off(self):
        self.dev.set_power('off')

    def toggle(self):
        self.dev.toggle()

    def bright(self, value):
        self.dev.set_bright(int(value))
    
    def set_default(self, *args):
        self.dev.set_default()
    
    def set_ct_abx(self, value):
        self.dev.set_ct_abx(int(value))
    
    def set_power(self, value):
        if type(value) is str:
            self.dev.set_power(value)
        elif type(value) is dict:
            self.dev.set_power(value.get('power'),
                               efx=value.get('efx', 'smooth'),
                               duration=value.get('duration', 500),
                               mode=value.get('mode', 0))

    def set_scene(self, value):
        if value is dict and {'scene_class', 'args'}.issubset(value):
            self.dev.set_scene(value['scene_class'], value['args'])

class ColorDev(White):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.cmd['set_rgb'] = self.set_rgb
        self.cmd['set_color'] = self.set_color
        self.dev = Color(ip='auto', sid=self.sid)
    
    def set_rgb(self, rgb):
        self.dev.set_rgb(rgb.get('red'), rgb.get('green'), rgb.get('blue'))
        
    def set_color(self, irgb):
        self.dev.set_color(irgb)
        
class Bslamp1Dev(ColorDev):
    pass

class DeskLampDev(White):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.dev = DeskLamp(ip='auto', sid=self.sid)