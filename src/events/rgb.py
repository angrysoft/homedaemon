from event import EventBase

class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'rgb'
        self._type = 'command'

    def start(self):
        self.send('F.{}'.format(self.args))
        print('F.{}'.format(self.args))


