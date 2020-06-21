from .base import Dummy
from pyiot.sony import Bravia

class Driver:
    def __new__(cls, model, sid, config, daemon):
        dev = {'KDL-48W585B': Bravia}.get(model, Dummy)(config.get('ip'),
                                                        config.get('mac'),
                                                        sid=sid,
                                                        model=model)
        daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev



