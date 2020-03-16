from .base import Dummy
from pyxiaomi.yeelight import DeskLamp, Bslamp1, Color, YeelightError

class YeeligthDevice:
    def __new__(cls, data, daemon):
        try:
            dev = {'color': Color,
                   'bslamp1': Bslamp1,
                   'desklamp': DeskLamp}.get(data.get('model'), Dummy)(data['sid'])
            daemon.bus.on('write', dev.sid, dev.write)
            dev.watcher.add_report_handler(daemon.bus.emit_cmd)
            return dev
        except YeelightError as err:
            daemon.logger.error(f'Error {err}')
