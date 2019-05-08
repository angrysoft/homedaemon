from homedaemon.events import EventBase
from homedaemon.devices import Device


class Event(EventBase):
    def __init__(self, daemon):
        super(Event, self).__init__(daemon)
        self._event = 'write'
        self._type = 'command'

    def do(self, data):
        self.daemon.logger.info(f"write event {data.get('model')} {data.get('data')}")
        dev_data = self.daemon.devices.get(data.get('sid'))
        if not dev_data:
            self.daemon.logger.warning(
                    f"The Device model={data.get('model')} with sid={data.get('sid')} are not registered ")
            return
        try:
            with self.lock:
                device = Device(dev_data)
                device.do(token=self.daemon.token, cmd=data.get('data'))
                del device
        except OSError as e:
            print(e)

        # if ret:
        #     self.daemon.queue.put(ret)
