from __future__ import annotations
from .base import DriverInterface
from pyiot.zigbee import ZigbeeDevice, ZigbeeGateway
from pyiot.zigbee.aqaragateway import AqaraGateway
from pyiot.xiaomi.aqara import Gateway, CtrlNeutral, CtrlNeutral2, SensorHt, WeatherV1, Magnet, \
    SensorMotionAq2, SensorSwitchAq2, Plug, Switch
from homedaemon.config import Config
from homedaemon.bus import Bus
from typing import Optional

conf = Config()
bus = Bus()
# gateway:GatewayInterface = GatewayInterface()
# gateway_conf = conf.get(gateway.sid)
# gateway.password = gateway_conf.get('gwpasswd')

class GatewayInstance:
    gateway: Optional[ZigbeeGateway] = None
    def __new__(cls) -> ZigbeeGateway:
        if GatewayInstance.gateway is None:
            GatewayInstance.gateway = AqaraGateway(gwpasswd=conf['7c49eb17b2a0']['password'])
            GatewayInstance.gateway.watcher.add_report_handler(bus.emit_cmd)
        return GatewayInstance.gateway


class Driver(DriverInterface):
    def __new__(cls, model:str, sid: str, config: Config):
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
            'gateway': Gateway,
            'switch': Switch}.get(model, ZigbeeDevice)(sid=sid, gateway=gw)
        bus.add_trigger(f'write.{dev.status.sid}.*.*', dev.execute)
        return dev