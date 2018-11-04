from house.event import EventBase


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'movie'
        self._type = 'scene'

    def start(self):
        if self.args == 'on':
            self.on()
        elif self.args == 'off':
            self.off()

    def on(self):
        self.send('F.{}'.format('0.0.255'))

    def off(self):
        pass


