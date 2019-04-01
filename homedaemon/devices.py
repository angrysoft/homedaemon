class Device:
    def __init__(self, data):
        model = data.get('model')
        self.device = None
        if model == 'ctrl_neutral1':
            pass
        elif model == 'ctrl_neutral2':
            pass
        elif model == '86sw1':
            pass
        elif model == '86sw2':
            pass
        elif model == 'sensor_ht':
            pass
        elif model == 'rgbw_light':
            pass
        elif model == 'magnet':
            pass
        elif model == 'motion':
            pass
        elif model == 'plug':
            pass
        elif model == 'switch':
            pass
        elif model == 'gateway':
            pass
        elif model == 'dallastemp':
            pass
        elif model == 'rgbstrip':
            pass


class BaseDevice:
    def __init__(self):
        self.model = None
        self.name = ''
        self.futures = list()


class GenericRgb(BaseDevice):
    def set_color(self):
        pass

    def set_dimmer(self):
        pass


class RgbLedStrip(GenericRgb):
    pass


class BedSideLamp(GenericRgb):
    pass


class YeelightBulb(BaseDevice):
    pass


class AquraBaseDevice:
    def __init__(self):
        super(AquraBaseDevice, self).__init__()
        self._voltage = -1
        self.low_voltage = 200
        self.writeable  = False

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = value


class Switch(AquraBaseDevice):
    def __init__(self):
        super(Switch, self).__init__()
        self.futures = ['click', 'double_click']

    def click(self):
        pass

    def double_click(self):
        pass


