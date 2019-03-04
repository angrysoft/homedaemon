from homedaemon.event import EventBase


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'heartbeat'
        self._type = 'command'

    def do(self, data):
        print(data)
        # Update device in database
        if data.get('model') == 'gateway':
            pass
            # self.daemon({'cmd': 'write',
            #              'model': 'gateway',
            #              'sid': data.get('sid'),
            #              'data': {'token': data.get('token'),
            #                       'ip': data.get('data').get('ip')}})


