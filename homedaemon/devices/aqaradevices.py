from . import BaseDevice, ButtonOnOff, ButtonToggleOnOff
from aquara import Gateway
import json
from datetime import datetime

aqara_models = (
    'ctrl_neutral1',
    'ctrl_neutral2',
    '86sw1',
    '86sw2',
    'sensor_ht',
    'weather.v1',
    'magnet',
    'sensor_motion.aq2',
    'sensor_switch.aq2',
    'plug',
    'gateway',
    
    )
    

class AqaraDevice:
    pass

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
        self.channel_0 = ButtonOnOff('channel_0', self.write)

class CtrlNeutral2(CtrlNeutral):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.channel_1 = ButtonOnOff('channel_1', self.write)
    
    def all_on(self):
        self.write({'data': {'channel_0': 'on', 'channel_1': 'on'}})
        
    def all_off(self):
        self.write({'data': {'channel_0': 'off', 'channel_1': 'off'}})


class Plug(AqaraBaseDevice):
    def __init__(self, data, daemon):
        super(Plug, self).__init__(data, daemon)
        self.power = ButtonToggleOnOff('status', self.write)
        self.writeable = True


class SensorSwitchAq2(AqaraBaseDevice):
    pass


class AqaraGateway(AqaraBaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.writeable = True

    def heartbeat(self, data):
        self.daemon.token = data.get('token')


class SensorMotionAq2(AqaraBaseDevice):
    
    def report(self, data):
        if 'status' in data['data']:
            data['data']['when'] = datetime.now().isoformat()
        self.update_dev_data(data['data'])
    
    @property
    def lux(self):
        return self.daemon.device_data[self.sid].get['lux']
