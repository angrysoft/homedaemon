from homedaemon.events import EventBase


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'timers'
        self._type = 'command'

    def start(self):
        pass
        # presence