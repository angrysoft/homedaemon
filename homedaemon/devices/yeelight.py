from homedaemon.bus import Bus
from pyiot.xiaomi.yeelight import DeskLamp, Bslamp1, Color, YeelightDev
from pyiot.exceptions import DeviceIsOffline
from homedaemon.logger import Logger


logger = Logger()
bus = Bus()


class Driver:
    def __new__(cls, model, sid, config):
        try:
            dev = {'color': Color,
                   'bslamp1': Bslamp1,
                   'desklamp': DeskLamp}.get(model, YeelightDev)(sid)
            bus.add_trigger(f'execute.{dev.status.sid}.*.*', dev.execute)
            dev.watcher.add_report_handler(bus.emit_cmd)
            return dev
        except DeviceIsOffline as err:
            logger.error(f'Error {err}')
