from homedaemon.events import EventBase
from homedaemon.devices import Device
from threading import current_thread


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'write'
        self._type = 'command'

    def do(self, data):
        with self.lock:
            print(f"write event {data.get('model')} {data.get('data')} {current_thread()}")
            dev_data = self.daemon.devices.get(data.get('sid'))
            if not dev_data:
                self.daemon.logger.warning(
                        f"The Device model={data.get('model')} with sid={data.get('sid')} are not registered ")
                return
            device = Device(dev_data)
            ret = device.do(token=self.daemon.token, cmd=data.get('data'))
            if ret:
                self.daemon.queue.put(ret)
