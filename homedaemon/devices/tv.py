from .base import BaseDevice, Dummy
from pytvremote import Bravia

class TvDevice:
    def __new__(cls, data, daemon):
        dev = {'KDL-48W585B': Bravia}.get(data.get('model'), Dummy)(data.get('ip'), data.get('mac'))
        daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev



