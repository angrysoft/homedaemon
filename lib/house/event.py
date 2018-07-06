class EventBase:
    def __init__(self):
        self._event = 'event'
        self.ctrl = None
        self.args = None
        self._type = ''

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._event

    def send(self, s):
        cmd = '{}\n'.format(s)
        self.ctrl.write(cmd.encode())

    def run(self, ctrl, args=None):
        self.ctrl = ctrl
        self.args = args
        self.start()

    def start(self):
        pass
