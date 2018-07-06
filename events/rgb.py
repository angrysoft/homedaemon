from house.event import EventBase
from house.rgb import RGB


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'rgb'
        self._type = 'command'
        self.rgb = RGB()

    def start(self):
        self.rgb.setRgb(self.args)
        self.send(self.rgb.toSend())


