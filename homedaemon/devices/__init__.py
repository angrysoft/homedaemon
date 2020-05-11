# from .aqaradevices import AqaraDevice
# from .yeelightdevices import YeeligthDevice
# from .philipsdevices import PhilipsDevice
# from .sonoffdevices import SonoffDevice
# from .tv import TvDevice
# from .custom import CustomDevice
# from .computer import ComputerDevice
# from .rgb import RgbDevice
# from .virtual import VirtualDevice
# from .scenes import SceneDevice
import importlib


class Devices:
    def __init__(self):
        self.drv = dict()
        self._devices = dict()
    
    # def register(self, data, daemon):
    #     daemon.debug(f"Loading....{data['sid']} : {data.get('name')}")
    #     device = {
    #         'aqara': AqaraDevice,
    #         'yeelight': YeeligthDevice,
    #         'custom': CustomDevice,
    #         'tv': TvDevice,
    #         'rgb': RgbDevice,
    #         'philips_light': PhilipsDevice,
    #         'sonoff': SonoffDevice,
    #         'scenes': SceneDevice,
    #         'virtual': VirtualDevice
    #         }.get(data.get('family'), self._unknown_device_family)(data, daemon)
    #     if device:
    #         self._devices[data['sid']] = device
    #         return True
    #     else:
    #         return False
    
    def register_devices(self, devices_list, daemon):
        _loaded = list()
        for dev in devices_list:
            drv_name = dev.get("family")
            try:
                daemon.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')}")
                self.load_driver(drv_name)
            except ImportError as err:
                daemon.logger.error(f"Driver not found {err}")
            self.register_dev(dev)
        return _loaded
    
    
    
    def register_dev(self, dev):
        pass
    
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


class Drivers:
    devices_drivers = dict()
    
    def get_driver(self, device_family, device_model):
        self._register_driver(device_family)
        
    
    def _register_driver(self, dev_family):
        if not dev_family in self.devices_drivers:
            drv_mod = importlib.import_module(f'homedaemon.devices.{dev_family}')
            self.devices_drivers[dev_family] = drv_mod.Driver