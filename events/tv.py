from house.event import EventBase
from house.bravia import Bravia


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'tv'
        self._type = 'command'

    def start(self):
        b = Bravia('192.168.1.129')
        b.macAddress = 'fc:f1:52:2a:9b:1e'
        print(self.args)
        if self.args == 'PowerOn':
            b.powerOn()
        else:
            if b.isOn():
                b.sendCommand(self.args)
