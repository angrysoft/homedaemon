from threading import RLock

class EventBase:
    def __init__(self, daemon):
        self._event = 'event'
        self.ctrl = None
        self.args = None
        self._type = ''
        self.daemon = daemon
        self.lock = RLock()

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._event

    def do(self, data):
        pass

    def update_dev_data(self, data):
        sid = data.get('sid')
        info = data.get('data')
        if sid and info:
            doc = self.daemon.device_data.get(sid)
            if doc:
                doc.update(info)
                self.daemon.device_data.save(doc)
                print('update db')

