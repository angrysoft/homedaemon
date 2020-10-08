from pyiot.sonoff import DiyPlug
from homedaemon.bus import Bus


bus = Bus()


class Driver:
    def __new__(cls, model, sid, config):
        dev = {'diy_plug': DiyPlug}.get(model)(sid)
        bus.add_trigger(f'execute.{dev.status.sid}.*.*', dev.execute)
        dev.watcher.add_report_handler(bus.emit_cmd)
        return dev