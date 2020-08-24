from .base import Dummy
from pyiot.xiaomi.philips_bulb import PhilipsBulb, PhilipsBulbException
from homedaemon.bus import Bus

bus = Bus()

class Driver:
    def __new__(cls, model, sid, config):
        try:
            dev = {'philips.light.candle': PhilipsBulb}.get(model, Dummy)(token=config['token'], sid=sid)
            bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
            dev.add_report_handler(bus.emit_cmd)
            return dev
        except PhilipsBulbException as err:
            logger.error(err)