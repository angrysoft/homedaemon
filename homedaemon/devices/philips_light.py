from .base import Dummy
from pyiot.xiaomi.philips_bulb import PhilipsBulb, PhilipsBulbException

class Driver:
    def __new__(cls, model, sid, config, daemon):
        try:
            dev = {'philips.light.candle': PhilipsBulb}.get(model, Dummy)(token=config['token'], sid=sid)
            daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
            dev.add_report_handler(daemon.bus.emit_cmd)
            return dev
        except PhilipsBulbException as err:
            daemon.logger.error(err)