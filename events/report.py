from homedaemon.event import EventBase


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'report'
        self._type = 'command'

    def do(self, data):
        pass
        # print(data)
        # if data.get('model') == 'gateway':


