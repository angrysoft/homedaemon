from pyiot.sonoff import DiyPlug
from .base import Dummy
from homedaemon.bus import Bus


bus = Bus()


class Driver:
    def __new__(cls, model, sid, config):
        dev = {'diy_plug': DiyPlug}.get(model, Dummy)(sid)
        bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        dev.watcher.add_report_handler(bus.emit_cmd)
        return dev