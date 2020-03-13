from .base import Dummy
from pyxiaomi.philips_bulb import PhilipsBulb, PhilipsBulbException

class YeeligthDevice:
    def __new__(cls, data, daemon):
        try:
            dev = {'philips_light': PhilipsBulb}.get(data.get('model'), Dummy)(sid=data['sid'], token=data['token'])
            daemon.bus.on('write', dev.sid, dev.write)
            dev.add_report_handler(daemon.bus.emit_cmd)
            return dev
        except PhilipsBulbException as err:
            daemon.logger.error(err)