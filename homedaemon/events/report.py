from homedaemon.events import EventBase
import json


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'report'
        self._type = 'command'

    def do(self, data):
        self.daemon.webserv.send(json.dumps(data))
        self.update_dev_data(data)
        print(data)


