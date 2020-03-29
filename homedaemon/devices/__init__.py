from .aqaradevices import AqaraDevice
from .yeelightdevices import YeeligthDevice
from .philipsdevices import PhilipsDevice
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
            'philips_light': PhilipsDevice,
            # 'sonoff': SonoffDevice,
            # 'scenes': SeceneDevice,
            'virtual': VirtualDevice
            }.get(data.get('family'), self._unknown_device_family)(data, daemon)
        if device:
            self._devices[data['sid']] = device
            return True
        else:
            return False
    
    def get(self, key, ret=None):
        try:
            return self._devices[key]
        except KeyError:
            return ret            
    
    def _unknown_device_family(self, data, *args):
        return None
        # raise ValueError(f"Unkonown deivce family : {data.get('family')} {data}")
    
    def __contains__(self, key):
        return key in self._devices
    
    def __getitem__(self, key):
        return self._devices[key]
