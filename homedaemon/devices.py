class Device:
    def __new__(cls, data):
        model = data.get('model')
        # self.device = None
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
        elif model == 'weather.v1t':
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
            pass
        elif model == 'switch':
            pass
        elif model == 'gateway':
            return Gateway(data)
        elif model == 'dallastemp':
            pass
        elif model == 'rgbstrip':
            pass
        raise ValueError(f'unrecognized device {model}')


class BaseDevice:
    def __init__(self):
        self.model = None
        self.name = ''
        self.futures = list()


class AquraBaseDevice(BaseDevice):
    def __init__(self):
        super(AquraBaseDevice, self).__init__()
        self._voltage = 3300
        self.low_voltage = 2800
        self.writeable = False

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = value


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


class Switch(AquraBaseDevice):
    def __init__(self):
        super(Switch, self).__init__()
        self.futures = ['click', 'double_click']

    def click(self):
        pass

    def double_click(self):
        pass


class Gateway(AquraBaseDevice):
    def __init__(self, data):
        super(Gateway, self).__init__()
        self.writeable = True




if __name__ == '__main__':
    test = {'cmd': 'report', 'model': 'gateway', 'sid': '7c49eb17b2a0', 'short_id': 0,
            'data': {'rgb': 0, 'illumination': 293}}
    test_txt = '{"cmd": "report", "model": "gateway", "sid": "7c49eb17b2a0", ' \
               '"short_id": 0, "data": {"rgb": 0, "illumination": 293}}'
    # dev = Device(test)
    # print(type(dev))
    import json
    print(json.loads(test_txt))
