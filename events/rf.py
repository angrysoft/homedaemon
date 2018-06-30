from house.event import EventBase
from house.rf import Rf


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'rf'
        self._type = 'command'

    def start(self):
        self.send(Rf.code(self.args))


