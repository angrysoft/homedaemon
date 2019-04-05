class EventBase:
    def __init__(self, daemon):
        self._event = 'event'
        self.ctrl = None
        self.args = None
        self._type = ''
        self.daemon = daemon

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
            result = self.daemon.device_data.update_one({'sid': sid}, {'$set': data})
            if result.matched_count < 1:
                self.daemon.logger.warning(
                    f"The Device model={data.get('model')} with sid={data.get('sid')} are not registered ")
