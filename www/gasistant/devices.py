import json
import pprint
from pycouchdb import Server


def get_devices_list():
    srv = Server()
    devicesdb = srv.db('devices')
    devices_list = list()
    for dev in devicesdb:
        model = dev.get('model')
        devinfo = None
        if model in ['bslamp1', 'color']:
            devinfo = Bslamp1(dev)
        elif model == 'ctrl_neutral1':
            devinfo = Ctrl1(dev)
        elif model == 'ctrl_neutral2':
            devinfo = Ctrl1(dev)
            devinfo.id += '.0'
            devinfo.name['name'] += ' channel 0'
            devices_list.append(devinfo.__dict__)
            devinfo = Ctrl1(dev)
            devinfo.id += '.1'
            devinfo.name['name'] += ' channel 1'
        elif model == 'plug':
            devinfo = Plug(dev)
    
        if devinfo:
            devices_list.append(devinfo.__dict__)
    return devices_list      

class GoogleDevice:
    def __init__(self, data):
        self.id = data.get('_id')
        self.type = ''
        self.traits = list()
        self.name = {
            'defaultNames': [],
            'name': data.get('name'),
            'nicknames': []
        }
        self.willReportState = False
        self.roomHint = ''
        self.deviceInfo = {
            'manufacturer': data.get('family'),
            'model': data.get('model'),
            'hwVersion': '',
            'swVersion': ''
        }
        self.customData = {}
        self.attributes = {}
    


class Bslamp1(GoogleDevice):
    def __init__(self, data):
        super().__init__(data)
        self.type = 'action.devices.types.LIGHT'
        self.traits.append('action.devices.traits.OnOff')
        self.traits.append('action.devices.traits.Brightness')
        self.traits.append('action.devices.traits.ColorSetting')
        self.attributes = {
            "colorModel": "rgb",
            "colorTemperatureRange": {
                "temperatureMinK": 1700,
                "temperatureMaxK": 6500
                }
        }


class Color(Bslamp1):
    pass


class Ctrl1(GoogleDevice):
    def __init__(self, data):
        super().__init__(data)
        self.type = 'action.devices.types.LIGHT'
        self.traits.append('action.devices.traits.OnOff')


class Plug(GoogleDevice):
    def __init__(self, data):
        super().__init__(data)
        self.type = 'action.devices.types.OUTLET'
        self.traits.append('action.devices.traits.OnOff')
        