from .base import Dummy
from pyxiaomi.yeelight import DeskLamp, Bslamp1, Color, YeelightError

class YeeligthDevice:
    def __new__(cls, data, daemon):
        try:
            dev = {'color': Color,
                   'bslamp1': Bslamp1,
                   'desklamp': DeskLamp}.get(data.get('model'), Dummy)(sid=data['sid'])
            daemon.bus.on('write', dev.sid, dev.write)
            return dev
        except YeelightError as err:
            daemon.logger.error(err)
