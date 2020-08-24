from .base import DriverInterface, Dummy
from pyiot.xiaomi.aqara import *
# from pyiot.base import BaseDevice
from homedaemon.config import Config
from homedaemon.bus import Bus

conf = Config()
bus = Bus()
# gateway:GatewayInterface = GatewayInterface()
# gateway_conf = conf.get(gateway.sid)
# gateway.password = gateway_conf.get('gwpasswd')

class GatewayInstance:
    gateway = None
    def __new__(cls):
        if GatewayInstance.gateway is None:
            GatewayInstance.gateway = Gateway(gwpasswd=conf['7c49eb17b2a0']['password'])
            GatewayInstance.gateway.watcher.add_report_handler(bus.emit_cmd)
        return GatewayInstance.gateway

# class Driver(DriverInterface):
    
#     def __new__(cls, model, sid, config) -> BaseDevice:
#         gw = GatewayInstance()
#         dev:BaseDevice = {
#             'ctrl_neutral1': CtrlNeutral,
#             'ctrl_neutral2': CtrlNeutral2,
#             'sensor_ht': SensorHt,
#             'weather.v1': WeatherV1,
#             'magnet': Magnet,
#             'sensor_motion.aq2': SensorMotionAq2,
#             'sensor_switch.aq2': SensorSwitchAq2,
#             'plug': Plug,
#             'switch': Switch,
#             'gateway': Gateway}.get(model, BaseDevice)(sid=sid, gateway=gateway)
#         bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
#         return dev

class Driver(DriverInterface):
    def __new__(cls, model, sid, config):
        gw = GatewayInstance()
        dev = {
            'ctrl_neutral1': CtrlNeutral,
            'ctrl_neutral2': CtrlNeutral2,
            'sensor_ht': SensorHt,
            'weather.v1': WeatherV1,
            'magnet': Magnet,
            'sensor_motion.aq2': SensorMotionAq2,
            'sensor_switch.aq2': SensorSwitchAq2,
            'plug': Plug,
            'switch': Switch,
            'gateway': cls.get_gateway}.get(model, Dummy)(sid=sid, gateway=gw)
        bus.add_trigger(f'write.{dev.sid}.*.*', dev.write)
        return dev
    
    @classmethod
    def get_gateway(cls, **kwargs):
        return kwargs['gateway']