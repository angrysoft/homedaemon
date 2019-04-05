from homedaemon.events import EventBase
from homedaemon.bravia import Bravia
from aquara import Gateway
from yeelight import Bulb


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'write'
        self._type = 'command'
        self.gateway = Gateway('cjvt7wr3q7df72rq')
        self.aquara_devs = ['ctrl_neutral2', 'plug']
        self.yeelight_devs = ['bslamp', 'color']
        self.arduino_devs = ['ledstrip']

    def do(self, data):
        print('write', data)
        model = data.get('model')
        dev_data = data.get('data')

        if model in self.aquara_devs:
            ret = self.gateway.write_device(data.get('model'), data.get('sid'), data.get('short_id'), dev_data)
        elif model in self.yeelight_devs:
            pass
        elif model in self.arduino_devs:
            pass
        elif model == 'bravia':
            b = Bravia('192.168.1.129')
            b.mac_address = 'fc:f1:52:2a:9b:1e'
            if dev_data.get('button') == 'PowerOn':
                b.power_on()
            else:
                if b.is_on():
                    b.send_command(dev_data.get('button'))
        elif model == 'ledstrip':
            pass

        if ret:
            self.daemon._queue_put(ret)



