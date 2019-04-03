from homedaemon.events import EventBase


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'report'
        self._type = 'command'

    def do(self, data):
        print(data, self.daemon.token)
        # if data.get('model') == 'gateway':


