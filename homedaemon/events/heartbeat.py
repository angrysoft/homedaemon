from homedaemon.events import EventBase


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'heartbeat'
        self._type = 'command'

    def do(self, data):
        if data.get('model') == 'gateway':
            if 'token' in data:
                self.daemon.token = data.get('token')
        else:
            sid = data.get('sid')
            info = data.get('data')
            if sid and info:
                result = self.daemon.devices.update_one({'sid': sid}, {'$set': data})
                if result.matched_count < 1:
                    self.daemon.logger.warning(
                        f"The Device model={data.get('model')} with sid={data.get('sid')} are not registered ")



