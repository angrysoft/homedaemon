
class Device:
    def __new__(cls, data, config={}):
        model = data.get('model')
        if model == 'ctrl_neutral1':
            from .aquaradevices import CtrlNeutral
            return CtrlNeutral(data, config)
        elif model == 'ctrl_neutral2':
            from .aquaradevices import CtrlNeutral2
            return CtrlNeutral2(data, config)
        elif model == '86sw1':
            pass
        elif model == '86sw2':
            pass
        elif model == 'sensor_ht':
            pass
        elif model == 'weather.v1':
            pass
        elif model == 'rgbw_light':
            pass
        elif model == 'magnet':
            pass
        elif model == 'motion':
            pass
        elif model == 'sensor_motion.aq2':
            pass
        elif model == 'plug':
            from .aquaradevices import Plug
            return Plug(data, config)
        elif model == 'switch':
            pass
        elif model == 'gateway':
            pass
        elif model == 'dallastemp':
            pass
        elif model == 'rgbstrip':
            from .color import RgbStrip
            return RgbStrip(data)
        elif model == 'bravia':
            from .tv import BraviaTv
            return BraviaTv(data)
        elif model in ['color', 'bslamp1']:
            from .yeelightdevices import YeeligthDevice
            return YeeligthDevice(data)
        else:
            raise ValueError(f'unrecognized device {model}')


class BaseDevice:
    def __init__(self, data):
        self.model = data.get('model')
        self.name = data.get('name')
        self.sid = data.get('sid')

    def do(self, **kwargs):
        print(kwargs)


class GenericRgb(BaseDevice):
    def set_color(self):
        pass

    def set_dimmer(self):
        pass
