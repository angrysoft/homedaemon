from . import BaseDevice
from aquara import Gateway


class AquraBaseDevice(BaseDevice):
    def __init__(self, data):
        super(AquraBaseDevice, self).__init__(data)
        self._voltage = 3300
        self.low_voltage = 2800
        self.writeable = False
        self.short_id = data.get('short_id')
        self.gateway = Gateway(gwpasswd='cjvt7wr3q7df72rq')

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = value

    def _write(self, token, data):
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
    def __init__(self, data):
        super(CtrlNeutral, self).__init__(data)
        self.writeable = True

    def do(self, token, cmd):
        if 'channel_0' in cmd:
            self.channel_0(token, cmd.get('channel_0'))

    def channel_0(self, token, value):
        self._write(token, {'channel_0': value})


class CtrlNeutral2(CtrlNeutral):

    def do(self, token, cmd):
        if 'channel_0' in cmd:
            self.channel_0(token, cmd.get('channel_0'))
        if 'channel_1' in cmd:
            self.channel_1(token, cmd.get('channel_1'))

    def channel_1(self, token, value):
        self._write(token, {'channel_1': value})


class Plug(AquraBaseDevice):
    def __init__(self, data):
        super(Plug, self).__init__(data)
        self._status = None

    def do(self, token, cmd):
        if 'status' in cmd:
            self.status(token, cmd.get('status'))

    def status(self, token, value):
        self._write(token, {'status': value})
