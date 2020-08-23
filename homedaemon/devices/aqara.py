from .base import DriverInterface
from pyiot.xiaomi.aqara import *
from pyiot.base import BaseDevice
from homedaemon.config import Config
from homedaemon.bus import Bus

conf = Config()
bus = Bus()
gateway:GatewayInterface = GatewayInterface()
gateway_conf = conf.get(gateway.sid)
gateway.password = gateway_conf.get('gwpasswd')

class Driver(DriverInterface):
    
    def __new__(cls, model, sid, config) -> BaseDevice:
        gw = GatewayInstance(daemon)
        dev:BaseDevice = {
            'ctrl_neutral1': CtrlNeutral,
            'ctrl_neutral2': CtrlNeutral2,
            'sensor_ht': SensorHt,
            'weather.v1': WeatherV1,
            'magnet': Magnet,
            'sensor_motion.aq2': SensorMotionAq2,
            'sensor_switch.aq2': SensorSwitchAq2,
            'plug': Plug,
            'switch': Switch,
            'gateway': Gateway}.get(model, BaseDevice)(sid=sid, gateway=gateway)
        bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev
