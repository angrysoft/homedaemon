from pyiot import BaseDevice
from pyiot.xiaomi.philips_bulb import PhilipsBulb
from pyiot.exceptions import DeviceIsOffline
from homedaemon.bus import Bus

bus = Bus()

class Driver:
    def __new__(cls, model, sid, config):
        try:
            dev = {'philips.light.candle': PhilipsBulb}.get(model, BaseDevice)(token=config['token'], sid=sid)
            bus.add_trigger(f'execute.{dev.status.sid}.*.*', dev.execute)
            dev.add_report_handler(bus.emit_cmd)
            return dev
        except DeviceIsOffline as err:
            logger.error(err)