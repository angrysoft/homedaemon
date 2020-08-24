from .base import Dummy
from pyiot.sony import Bravia
from homedaemon.bus import Bus


bus = Bus()



class Driver:
    def __new__(cls, model, sid, config):
        dev = {'KDL-48W585B': Bravia}.get(model, Dummy)(config.get('ip'),
                                                        sid=sid,
                                                        model=model)
        bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev



