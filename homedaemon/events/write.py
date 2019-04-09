from homedaemon.events import EventBase
from homedaemon.devices import Device


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'write'
        self._type = 'command'

    def do(self, data):
        print('write event', data)
        dev_data = self.daemon.devices.find_one({'sid': data.get('sid')})
        if not dev_data:
            self.daemon.logger.warning(
                    f"The Device model={data.get('model')} with sid={data.get('sid')} are not registered ")
            return
        device = Device(dev_data)
        ret = device.do(token=self.daemon.token, cmd=data.get('data'))
        if ret:
            self.daemon._queue_put(ret)




