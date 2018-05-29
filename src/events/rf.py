from event import EventBase

class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'rf'
        self._type = 'command'

    def start(self):
        self.send('W.{}'.format(self.args))
        print('W.{}'.format(self.args))


