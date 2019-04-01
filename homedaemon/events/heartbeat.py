from homedaemon.events import EventBase


class Event(EventBase):
    def __init__(self, db):
        super(Event, self).__init__(db)
        self._event = 'heartbeat'
        self._type = 'command'

    def do(self, data):
        print(data)
        # Update device in database
        # dev_data = data.get('data')

        # print(type(dev_data))
        if data.get('model') == 'gateway':
            pass
            # self.daemon({'cmd': 'write',
            #              'model': 'gateway',
            #              'sid': data.get('sid'),
            #              'data': {'token': data.get('token'),
            #                       'ip': data.get('data').get('ip')}})


