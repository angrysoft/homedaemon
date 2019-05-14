from . import BaseDevice
from aquara import Gateway


class AquraBaseDevice(BaseDevice):
    def __init__(self, data, daemon):
        super(AquraBaseDevice, self).__init__(data, daemon)
        self._voltage = 3300
        self.low_voltage = 2800
        self.writeable = False
        self.short_id = data.get('short_id')
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
            return 'Token is missing'
        if type(data) is not dict:
            raise ValueError('Data argument is not dict')
        if not self.writeable:
            raise PermissionError('Device is not writable')
        self.gateway.token = self.daemon.token
        self.gateway.write_device(self.model,
                                  self.sid,
                                  self.short_id,
                                  data)


class CtrlNeutral(AquraBaseDevice):
    def __init__(self, data, daemon):
        super(CtrlNeutral, self).__init__(data, daemon)
        self.writeable = True

    def channel_0(self, value):
        self.write({'channel_0': value})


class CtrlNeutral2(CtrlNeutral):

    def channel_1(self, value):
        self.write({'channel_1': value})


class Plug(AquraBaseDevice):
    def __init__(self, data, daemon):
        super(Plug, self).__init__(data, daemon)
        self._status = None
        self.writeable = True

    def status(self, value):
        self.write({'status': value})


class AquaraGateway(AquraBaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.writeable = True

    def heartbeat(self, data):
        self.daemon.token = data.get('token')
