import importlib
from os.path import isdir
from os import scandir
from homedaemon.config import Config
from homedaemon.logger import Logger
import json

class Devices:
    def __init__(self):
        self.drivers = Drivers()
        self._devices = dict()
        self._devices_fail_list =list()
        self.config = Config()
        self.logger = Logger()
    
    def register_devices(self, daemon):
        for dev in self.get_devices_list():
            self.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')}")
            # try:
            self.register_dev(dev, daemon)
            # except Exception as err:
                # self.logger.error(str(err))
            # daemon.loop.run_in_executor(None, self.register_dev, dev, daemon)
    
    def get_devices_list(self):
        ret = []
        try:
            _dir = scandir(path=self.config.get('devices_dir'))
            for _file in _dir:
                if _file.is_file and _file.name.endswith('.json'):
                    with open(_file.path) as dev_file:
                        ret.append(json.load(dev_file))
                        
        except FileNotFoundError as fnf:
            self.logger.error(f'Get devices list {fnf}')
        except NotADirectoryError as nd:
            self.logger.error(f'Get devices list {nd}')
        
        return ret
        
    def register_dev(self, dev, daemon):
        drv = self.drivers.get_driver(dev["family"])
        if drv:
            dev_instace = drv(dev['model'],
                              dev['sid'],
                              self.config.get(dev['sid']),
                              daemon)
            if dev_instace:
                dev_instace.name = dev.get('name', '')
                dev_instace.place = dev.get('place', '')
                self._devices[dev['sid']] = dev_instace
            
    def get(self, key, ret=None):
        try:
            return self._devices[key]
        except KeyError:
            return ret
    
    def get_devices_info_list(self):
        ret = list()
        for devitem in self._devices:
            dev = self.get(devitem)
            ret.append({'sid': dev.sid, 'model': dev.model,
                        'name': dev.name, 'place': dev.place,
                        'status': dev.device_status()})
        return ret
      
    def _unknown_device_family(self, data, *args):
        return None
    
    def __contains__(self, key):
        return key in self._devices
    
    def __getitem__(self, key):
        return self._devices[key]


class Drivers:
    devices_drivers = dict()
    
    def get_driver(self, device_family):
        self._register_driver(device_family)
        if device_family in self.devices_drivers:
            return self.devices_drivers[device_family]
        else:
            return None
    
    def _register_driver(self, dev_family):
        if not dev_family in self.devices_drivers:
            try:
                drv_mod = importlib.import_module(f'homedaemon.devices.{dev_family}')
                self.devices_drivers[dev_family] = drv_mod.Driver
            except ModuleNotFoundError:
                pass
