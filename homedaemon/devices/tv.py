from pyiot.sony.bravia import KDL48W585B
from homedaemon.bus import Bus


bus = Bus()



class Driver:
    def __new__(cls, model, sid, config):
        dev = {'KDL-48W585B': KDL48W585B}.get(model)(config.get('ip'))
        bus.add_trigger(f'execute.{dev.status.sid}.*.*', dev.execute)
        return dev



