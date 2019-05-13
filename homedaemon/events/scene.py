from homedaemon.events import SceneBase


class Event(SceneBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'report'
        self._type = 'command'

    def do(self, data):
        pass


