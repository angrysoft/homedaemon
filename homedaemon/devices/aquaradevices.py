from . import BaseDevice
from aquara import Gateway
import json


class AquraBaseDevice(BaseDevice):
    def __init__(self, data, daemon):
        super(AquraBaseDevice, self).__init__(data, daemon)
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
        print('write',
              self.model,
              self.sid,
              self.short_id,
              data)
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


class CtrlNeutral(AquraBaseDevice):
    def __init__(self, data, daemon):
        super(CtrlNeutral, self).__init__(data, daemon)
        self.writeable = True
        self._t0 = 0
        self.t1 = 0

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


class SensorSwitchAq2(AquraBaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self._status = None
        self.on_click = data.get('on_click')
        self.on_double_click = data.get('on_double_click')

    def report(self, data):
        # TODO info
        self.daemon.logger.info(str(data))
        self.daemon.notify_clients(json.dumps(data))
        data = data.get('data')
        event, arg = data.popitem()
        self.update_dev_data(data)
        return {'click': self.click,
                'double_click': self.double_click}.get(arg, self._unknown_cmd)()

    def click(self):
        if self.on_click is None:
            return
        self.daemon.queue.put({'sid': self.on_click,
                               'data': {'sid': self.sid, 'status': 'on'}})

    def double_click(self):
        if self.on_double_click is None:
            return
        self.daemon.queue.put({'sid': self.on_double_click,
                               'data': {'sid': self.sid, 'status': 'on'}})


class AquaraGateway(AquraBaseDevice):
    def __init__(self, data, daemon):
        super().__init__(data, daemon)
        self.writeable = True

    def heartbeat(self, data):
        self.daemon.token = data.get('token')


class SensorMotionAq2(AquraBaseDevice):
    def __init__(self, data, daemon):
        super(SensorMotionAq2, self).__init__(data, daemon)
        self.on_motion = data.get('on_motion')
        self.on_no_motion = dict()

        self.on_no_motion.update(data.get('on_no_motion', {}))

    def report(self, data):
        # TODO info
        self.daemon.logger.info(str(data))
        self.daemon.notify_clients(json.dumps(data))
        data = data.get('data')
        event, arg = data.popitem()
        self.update_dev_data(data)
        return {'no_motion': self.no_motion,
                'status': self.motion,
                'lux': self.lux}.get(event, self._unknown_cmd)(arg)

    def no_motion(self, _time):
        if _time in self.on_no_motion:
            self.daemon.queue.put({'sid': self.on_no_motion.get(_time),
                                   'data': {'sid': self.sid, 'status': 'on'}})

    def motion(self, arg):
        if self.on_motion is None:
            return
        self.daemon.queue.put({'sid': self.on_motion,
                               'data': {'sid': self.sid, 'status': 'on'}})

    def lux(self, arg):
        pass

