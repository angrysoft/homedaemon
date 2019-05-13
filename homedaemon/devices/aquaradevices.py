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

    def _write(self, token, data):
        if token is None:
            return 'Token is missing'
        if type(data) is not dict:
            raise ValueError('Data argument is not dict')
        if not self.writeable:
            raise PermissionError('Device is not writable')
        self.gateway.token = token
        self.gateway.write_device(self.model,
                                  self.sid,
                                  self.short_id,
                                  data)


class CtrlNeutral(AquraBaseDevice):
    def __init__(self, data, daemon):
        super(CtrlNeutral, self).__init__(data, daemon)
        self.writeable = True

    def do(self, **kwargs):
        if not {'token', 'cmd'}.issubset(kwargs):
            return
        if 'channel_0' in kwargs['cmd']:
            self.channel_0(kwargs['token'], kwargs['cmd']['channel_0'])

    def channel_0(self, token, value):
        self._write(token, {'channel_0': value})


class CtrlNeutral2(CtrlNeutral):

    def do(self, **kwargs):
        if not {'token', 'cmd'}.issubset(kwargs):
            return
        if 'channel_0' in kwargs['cmd']:
            self.channel_0(kwargs['token'], kwargs['cmd']['channel_0'])
        if 'channel_1' in kwargs['cmd']:
            self.channel_1(kwargs['token'], kwargs['cmd']['channel_1'])

    def channel_1(self, token, value):
        self._write(token, {'channel_1': value})


class Plug(AquraBaseDevice):
    def __init__(self, data, daemon):
        super(Plug, self).__init__(data, daemon)
        self._status = None
        self.writeable = True

    def do(self, **kwargs):
        if not {'token', 'cmd'}.issubset(kwargs):
            return
        if 'status' in kwargs['cmd']:
            self.status(kwargs['token'], kwargs['cmd']['status'])

    def status(self, token, value):
        self._write(token, {'status': value})


class AquaraGateway(AquraBaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.writeable = True

    def do(self, data):
        cmd = data.get('cmd')
        if cmd == 'heartbeat':
            self.daemon.token = data.get('token')
