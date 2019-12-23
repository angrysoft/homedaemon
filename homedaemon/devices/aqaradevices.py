from .base import BaseDevice
from aqara import Gateway
import json
from datetime import datetime
    

class AqaraDevice:
    def __new__(cls, data, daemon):
        return {
            'ctrl_neutral1': CtrlNeutral,
            'ctrl_neutral2': CtrlNeutral2,
            'sensor_ht': SensorHt,
            'weather.v1': WeatherV1,
            'magnet': Magnet,
            'sensor_motion.aq2': SensorMotionAq2,
            'sensor_switch.aq2': SensorSwitchAq2,
            'plug': Plug,
            'gateway': AqaraGateway}.get(data['model'], AqaraBaseDevice)(data, daemon)


class AqaraBaseDevice(BaseDevice):
    def __init__(self, data, daemon):
        super(AqaraBaseDevice, self).__init__(data, daemon)
        self._voltage = 3300
        self.low_voltage = 2800
        self.writeable = False
        self.short_id = data.get('short_id')
        self.name = data.get('name')
        self.gateway = Gateway(ip=self.daemon.config['gateway']['ip'],
                               gwpasswd=self.daemon.config['gateway']['password'])

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = value

    def write(self, data):
        if self.daemon.token is None:
            raise ValueError('Token is missing')
        if type(data) is not dict:
            raise ValueError('Data argument is not dict')
        if not self.writeable:
            raise PermissionError('Device is not writable')
        self.gateway.token = self.daemon.token
        self.gateway.write_device(self.model,
                                  self.sid,
                                  self.short_id,
                                  data.get('data'))
    


class CtrlNeutral(AqaraBaseDevice):
    def __init__(self, data, daemon):
        super(CtrlNeutral, self).__init__(data, daemon)
        self.writeable = True
        self.channel_0 = Button('channel_0', self)
        

class CtrlNeutral2(CtrlNeutral):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.channel_1 = Button('channel_1', self)
    
    def on(self):
        self.write({'data': {'channel_0': 'on', 'channel_1': 'on'}})
        
    def off(self):
        self.write({'data': {'channel_0': 'off', 'channel_1': 'off'}})


class Plug(AqaraBaseDevice):
    def __init__(self, data, daemon):
        super(Plug, self).__init__(data, daemon)
        self.power = Button('status', self)
        self.writeable = True


class SensorSwitchAq2(AqaraBaseDevice):
    pass


class SensorHt(AqaraBaseDevice):
    pass


class WeatherV1(AqaraBaseDevice):
    pass


class Magnet(AqaraBaseDevice):
    
    def update_dev_data(self, data):
        if 'status' in data['data']:
            data['data']['when'] = datetime.now().isoformat()
        super().update_dev_data(data)


class AqaraGateway(BaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.writeable = True

    def heartbeat(self, data):
        self.daemon.token = data.get('token')


class SensorMotionAq2(AqaraBaseDevice):
    
    def update_dev_data(self, data):
        if 'status' in data['data']:
            data['data']['when'] = datetime.now().isoformat()
        super().update_dev_data(data)
    
    @property
    def lux(self):
        return self.daemon.device_data[self.sid].get['lux']

class Button:
    def __init__(self, name, device):
        self.name = name
        self.device = device
        
    def on(self):
        self.device.write({'data': {self.name: 'on'}})

    def off(self):
        self.device.write({'data': {self.name: 'off'}})
    
    def toggle(self):
        self.device.write({'data': {self.name: 'toggle'}})
    
    def is_on(self):
        if self.device.get_value(self.name) == 'on':
            return True
        else:
            return False
        
    def is_off(self):
        if self.device.get_value(self.name) == 'off':
            return True
        else:
            return False