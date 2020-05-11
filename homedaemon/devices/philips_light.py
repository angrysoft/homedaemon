from .base import Dummy
from pyxiaomi.philips_bulb import PhilipsBulb, PhilipsBulbException

class PhilipsDevice:
    def __new__(cls, data, daemon):
        try:
            dev = {'philips.light.candle': PhilipsBulb}.get(data.get('model'), Dummy)(token=data['token'], sid=data['sid'])
            daemon.bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
            dev.add_report_handler(daemon.bus.emit_cmd)
            return dev
        except PhilipsBulbException as err:
            daemon.logger.error(err)