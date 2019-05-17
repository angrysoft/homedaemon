from threading import RLock, Thread
import json


class Device:
    def __new__(cls, data, daemon):
        model = data.get('model')
        if model == 'ctrl_neutral1':
            from .aquaradevices import CtrlNeutral
            return CtrlNeutral(data, daemon)
        elif model == 'ctrl_neutral2':
            from .aquaradevices import CtrlNeutral2
            return CtrlNeutral2(data, daemon)
        elif model == '86sw1':
            return BaseDevice(data, daemon)
        elif model == '86sw2':
            return BaseDevice(data, daemon)
        elif model == 'sensor_ht':
            return BaseDevice(data, daemon)
        elif model == 'weather.v1':
            return BaseDevice(data, daemon)
        elif model == 'rgbw_light':
            return BaseDevice(data, daemon)
        elif model == 'magnet':
            return BaseDevice(data, daemon)
        elif model == 'motion':
            return BaseDevice(data, daemon)
        elif model == 'sensor_motion.aq2':
            return BaseDevice(data, daemon)
        elif model == 'sensor_switch.aq2':
            return BaseDevice(data, daemon)
        elif model == 'plug':
            from .aquaradevices import Plug
            return Plug(data, daemon)
        elif model == 'switch':
            return BaseDevice(data, daemon)
        elif model == 'gateway':
            from .aquaradevices import AquaraGateway
            return AquaraGateway(data, daemon)
        elif model == 'dallastemp':
            return BaseDevice(data, daemon)
        elif model == 'rgbstrip':
            from .color import RgbStrip
            return RgbStrip(data, daemon)
        elif model == 'bravia':
            from .tv import BraviaTv
            return BraviaTv(data, daemon)
        elif model in ['color', 'bslamp1']:
            from .yeelightdevices import YeeligthDevice
            return YeeligthDevice(data, daemon)
        else:
            raise ValueError(f'unrecognized device {model}')


class BaseDevice:
    def __init__(self, data, daemon):
        self.daemon = daemon
        self.model = data.get('model')
        self.name = data.get('name')
        self.sid = data.get('sid')
        self.lock = RLock()

    def do(self, data):
        return {'write': self.write,
                'report': self.report,
                'heartbeat': self.heartbeat}.get(data.get('cmd'),
                                                 self._unknown_cmd)(data)

    def _unknown_cmd(self, data):
        self.daemon.logger.error(f'Unknown command:  {data}')

    def write(self, data):
        print('write',data)

    def heartbeat(self, data):
        print('heartbeat', data)

    def report(self, data):
        print(data)
        self.daemon.notify_clients(json.dumps(data))
        self.update_dev_data(data.get('data'))

    def update_dev_data(self, data):
        with self.lock:
            doc = self.daemon.device_data.get(self.sid)
            if doc:
                doc.update(data)
                self.daemon.device_data.save(doc)

