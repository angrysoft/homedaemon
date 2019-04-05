from homedaemon.events import EventBase


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'heartbeat'
        self._type = 'command'

    def do(self, data):
        if data.get('model') == 'gateway':
            if 'token' in data:
                self.daemon.token = data.get('token')
        else:
            self.update_dev_data(data)
