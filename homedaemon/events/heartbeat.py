from homedaemon.events import EventBase
from homedaemon.devicesdb import *


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
            dev = self.daemon.db.select(Devices).where(Devices.sid == data.get('sid', '-1')).first()
            if dev:
                self._update_info(data)
            else:
                self.daemon.logger.warning(
                    f"Device model={data.get('model')} with sid={data.get('sid')} not registered ")

    def _update_info(self, dev_info):
        print(dev_info)

