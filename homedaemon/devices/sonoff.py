from pyiot.sonoff import DiyPlug
from .base import Dummy


class Driver:
    def __new__(cls, data, daemon):
        dev = {'diy_plug': DiyPlug}.get(data.get('model'), Dummy)(data['sid'])
        daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        dev.watcher.add_report_handler(daemon.bus.emit_cmd)
        return dev