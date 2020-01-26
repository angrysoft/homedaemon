from .base import BaseDevice, ButtonOnOff, Dummy
from yeelight import DeskLamp, Bslamp1, Color, YeelightDev
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
        self.dev = YeelightDev(data.get('ip'))
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
        asyncio.run_coroutine_threadsafe(self.dev.set_power('on'), self.daemon.loop)

    def off(self):
        asyncio.run_coroutine_threadsafe(self.dev.set_power('off'), self.daemon.loop)

    def toggle(self):
        asyncio.run_coroutine_threadsafe(self.dev.toggle(), self.daemon.loop)

    def bright(self, value):
        asyncio.run_coroutine_threadsafe(self.dev.set_bright(int(value)), self.daemon.loop)
    
    def set_default(self, *args):
        asyncio.run_coroutine_threadsafe(self.dev.set_default(), self.daemon.loop)
    
    def set_ct_abx(self, value):
        asyncio.run_coroutine_threadsafe(self.dev.set_ct_abx(int(value)), self.daemon.loop)
    
    def set_power(self, value):
        if type(value) is str:
            asyncio.run_coroutine_threadsafe(self.dev.set_power(value), self.daemon.loop)
        elif type(value) is dict:
            asyncio.run_coroutine_threadsafe(self.dev.set_power(value.get('power'),
                                                                 efx=value.get('efx', 'smooth'),
                                                                 duration=value.get('duration', 500),
                                                                 mode=value.get('mode', 0)), self.daemon.loop)

    def set_scene(self, value):
        if value is dict and {'scene_class', 'args'}.issubset(value):
            asyncio.run_coroutine_threadsafe(self.dev.set_scene(value['scene_class'], value['args']), self.daemon.loop)

class ColorDev(White):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.cmd['set_rgb'] = self.set_rgb
        self.cmd['set_color'] = self.set_color
        self.dev = Color(self.ip)
    
    def set_rgb(self, rgb):
        asyncio.run_coroutine_threadsafe(self.dev.set_rgb(rgb.get('red'), rgb.get('green'), rgb.get('blue')), self.daemon.loop)
        
    def set_color(self, irgb):
        asyncio.run_coroutine_threadsafe(self.dev.set_color(irgb), self.daemon.loop)
        
class Bslamp1Dev(Color):
    pass

class DeskLampDev(White):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.dev = DeskLamp(self.ip)