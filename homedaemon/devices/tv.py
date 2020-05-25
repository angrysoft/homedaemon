from .base import Dummy
from pyiot.sony import Bravia

class Driver:
    def __new__(cls, data, daemon):
        dev = {'KDL-48W585B': Bravia}.get(data.get('model'), Dummy)(data.get('ip'), data.get('mac'))
        daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev



