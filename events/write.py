from homedaemon.event import EventBase
from homedaemon.bravia import Bravia
from aquara import Gateway


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'write'
        self._type = 'command'
        self.gateway = Gateway('cjvt7wr3q7df72rq')

    def do(self, data):
        print('write', data)
        model = data.get('model')
        dev_data = data.get('data')

        if model == 'gateway':
            pass
        elif model == 'ctrl_neutral2':
            pass
        elif model == 'plug':
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


