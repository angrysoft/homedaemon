from .aqaradevices import AqaraDevice
from .yeelightdevices import YeeligthDevice
from .tv import TvDevice
from .custom import CustomDevice
from .computer import ComputerDevice
from .rgb import RgbDevice
from .virtual import VirtualDevice


class Devices:
    def __init__(self):
        self._devices = dict()
    
    def load(self, data, daemon):
        device = {
            'aqara': AqaraDevice,
            'yeelight': YeeligthDevice,
            'custom': CustomDevice,
            'tv': TvDevice,
            'rgb': RgbDevice,
            'virtual': VirtualDevice
            }.get(data.get('family'), self._unknown_device_family)(data, daemon)
        self._devices[data['sid']] = device
    
    def _unknown_device_family(self, data):
        raise ValueError(f"Unkonown deivce family : {data.get('family')} {data}")
    
    def __contains__(self, key):
        return key in self._devices
    
    def __getitem__(self, key):
        return self._devices[key]
