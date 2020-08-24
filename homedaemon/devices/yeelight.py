from .base import Dummy
from homedaemon.bus import Bus
from pyiot.xiaomi.yeelight import DeskLamp, Bslamp1, Color, YeelightError
from homedaemon.logger import Logger


logger = Logger()
bus = Bus()


class Driver:
    def __new__(cls, model, sid, config):
        try:
            dev = {'color': Color,
                   'bslamp1': Bslamp1,
                   'desklamp': DeskLamp}.get(model, Dummy)(sid)
            bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
            dev.watcher.add_report_handler(bus.emit_cmd)
            return dev
        except YeelightError as err:
            logger.error(f'Error {err}')
