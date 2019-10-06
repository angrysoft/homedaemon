from . import BaseDevice
from aquara import Gateway
import json

class ButtonOnOff:
    def __init__(self, name, sid, write):
        self.name = name
        self.write = write

    def on(self):
        self.write({'data': {self.name: 'on'}})

    def off(self):
        self.write({'data': {self.name: 'on'}})


class ButtonToggleOnOff(ButtonOnOff):

    def toggle(self):
        self.write({'data': {self.name: 'toggle'}})


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
        self.channel_0 = ButtonOnOff('channel_0', self.sid, self.write)

class CtrlNeutral2(CtrlNeutral):

    @property
    def channel_1(self):
        return self.daemon.device_data[self.sid].get('channel_1')
    
    @channel_1.setter
    def channel_1(self, value):
        self.write({'data':{'channel_1': value}})


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
        self.on_motion_event = data.get('on_motion')
        self.on_no_motion_event = dict()
        self.on_no_motion_event.update(data.get('on_nomotion', {}))
        self.on_lux_event = data.get('on_lux')

    def report(self, data):
        # TODO info
        self.daemon.logger.info(str(data))
        self.daemon.notify_clients(json.dumps(data))
        data = data.get('data')
        event, arg = data.popitem()
        self.update_dev_data(data)
        return {'no_motion': self.on_no_motion,
                'status': self.on_motion,
                'lux': self.on_lux}.get(event, self._unknown_cmd)(arg)

    def on_no_motion(self, _time):
        if _time in self.on_no_motion_event:
            self.daemon.queue.put({'sid': self.on_no_motion_event.get(_time),
                                   'data': {'sid': self.sid, 'status': 'on'}})

    def on_motion(self, arg):
        if self.on_motion_event is None:
            return
        self.daemon.queue.put({'sid': self.on_motion_event,
                               'data': {'sid': self.sid, 'status': 'on'}})

    
    def on_lux(self, arg):
        if self.on_lux_event:
            self.daemon.queue.put({'sid': self.on_lux_event,
                                   'data': {'sid': self.sid, 'status': 'on'}})
        
    
    @property
    def lux(self):
        return self.daemon.device_data[self.sid].get['lux']
    


