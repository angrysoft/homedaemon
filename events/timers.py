from house.event import EventBase


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'timers'
        self._type = 'command'

    def start(self):
        self.send('T.0')
        self.send('T.1')
        self.send('L.0')
        # presence