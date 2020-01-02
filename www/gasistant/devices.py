import json
import pprint
from pycouchdb import Server


def get_devices_list():
    srv = Server()
    devicesdb = srv.db('devices')
    scenedb = srv.db('scenes')
    devices_list = list()
    for dev in devicesdb:
        model = dev.get('model')
        devinfo = None
        if model in ['bslamp1', 'color']:
            devinfo = Bslamp1(dev)
        elif model == 'ctrl_neutral1':
            devinfo = Ctrl1(dev)
        elif model == 'ctrl_neutral2':
            devinfo = Ctrl2(dev)
            devinfo.id += '.0'
            devinfo.name['name'] += ' channel 0'
            devices_list.append(devinfo.sync())
            devinfo = Ctrl2(dev)
            devinfo.id += '.1'
            devinfo.name['name'] += ' channel 1'
        elif model == 'plug':
            devinfo = Plug(dev)
    
        if devinfo:
            devices_list.append(devinfo.sync())
    for scene in scenedb:
        if scene.get('automatic') == False:
            sc = Scene(scene)
            devices_list.append(sc.sync())
            
    
    return devices_list


class QueryDevice:
    def __init__(self, sid):
        srv = Server()
        self.devbd = srv.db('device')
        self.datadb = srv.db('device-data')
        self.channel = None
        self.sid = sid
        if sid[-2] == '.':
            sid, channel = sid.rsplit('.', 1)
    
    def query(self):
        dev = self.devbd.get(self.sid)
        devdata = self.datadb.get(self.sid)
        model = dev.get('model')
        devinfo = None
        if model in ['bslamp1', 'color']:
            devinfo = Bslamp1(dev)
        elif model == 'ctrl_neutral1':
            devinfo = Ctrl1(dev)
        elif model == 'ctrl_neutral2':
            devinfo = Ctrl2(dev)
            return devinfo.query(devdata, self.channel)
        elif model == 'plug':
            devinfo = Plug(dev)
        
        return devinfo.query(devdata)
        
        
        
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
            'manufacturer': data.get('family', ''),
            'model': data.get('model', ''),
            'hwVersion': '',
            'swVersion': ''
        }
        self.customData = {}
        self.attributes = {}
    
    def sync(self):
        return {
            'id': self.id,
            'type': self.type,
            'traits': self.traits,
            'name': self.name,
            'willReportState': self.willReportState,
            'roomHint': self.roomHint,
            'deviceInfo': self.deviceInfo,
            'customData': self.customData,
            'attributes': self.attributes
        }
    
    def query(self, devdata):
        pass
    
    def exectute(self):
        pass
    
    def _power(self, status):
        return {'on': True, 'off': False}.get(status)
    


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
    
    def query(self, devdata):
        ret = {
            'on': self._power(devdata['power']),
            'online': True,
            'brightness': int(devdata['bright']),
            'spectrumRgb': devdata['rgb'],
            'temperatureK': devdata['ct']
        }
        # if devdata['color_mode'] == 2:
        #     ret['color'][]
        return ret


class Color(Bslamp1):
    pass


class Ctrl1(GoogleDevice):
    def __init__(self, data):
        super().__init__(data)
        self.type = 'action.devices.types.LIGHT'
        self.traits.append('action.devices.traits.OnOff')
    
    def query(self, devdata):
        ret = {
            'on': self._power(devdata['channel_0']),
            'online': True,
        }
        return ret
        

class Ctrl2(Ctrl1):
    def query(self, devdata, channel):            
        ret = {
            'on': self._power(devdata[f'channel_{channel}']),
            'online': True,
        }
        return ret


class Plug(GoogleDevice):
    def __init__(self, data):
        super().__init__(data)
        self.type = 'action.devices.types.OUTLET'
        self.traits.append('action.devices.traits.OnOff')
    
    def query(self, devdata):
        ret = {
            'on': self._power(devdata['status']),
            'online': True,
        }
        return ret

class Scene(GoogleDevice):
    def __init__(self, data):
        super().__init__(data)
        self.type = 'action.devices.types.SCENE'
        self.traits.append('action.devices.traits.Scene')
        self.attributes['sceneReversible'] = data.get('reversable', False)