class EventBase:
    def __init__(self, db):
        self._event = 'event'
        self.ctrl = None
        self.args = None
        self._type = ''
        self.db = db

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._event

    def do(self, data):
        pass