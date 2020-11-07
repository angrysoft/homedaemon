from __future__ import annotations
import importlib
from os import DirEntry, scandir
from homedaemon.config import Config
from homedaemon.logger import Logger
import json
from typing import Generator, Iterator, List, Dict, Any

class DriverInterface:
    pass

class Drivers:
    drivers_modules: Dict[str, object] = dict()
    
    def is_module_loaded(self, driver_module:str) -> bool:
        return driver_module in self.drivers_modules

    def get_driver(self, driver_class:str):
        return getattr(self.drivers_modules, driver_class)

    def load_driver_module(self, driver_module:str) -> None:
        try:
            drv_mod = importlib.import_module(driver_module)
            self.drivers_modules[driver_module] = drv_mod
        except ModuleNotFoundError:
            pass
        

              
class Devices:
    _instance = object = None
    
    def __new__(cls):
        if Devices._instance is None:
            cls.drivers: Drivers = Drivers()
            cls._devices: Dict[str, Drivers] = dict()
            cls._devices_fail_list: List[Dict[str,str]] = list()
            cls.config = Config()
            cls.logger: Logger = Logger()
            Devices._instance = object.__new__(cls)
        return cls._instance
    
    def register_devices(self) -> None:
        for dev in self.get_devices_info_list():
            self.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')} from {dev.get('place')}")
            self.register_dev(dev)

        
    def get_devices_info_list(self) -> Generator[Dict[str,Any], None, None]:
        try:
            _dir: Iterator[DirEntry[str]] = scandir(path=self.config.get('devices_dir'))
            for _file in _dir:
                if _file.is_file and _file.name.endswith('.json'):
                    with open(_file.path) as dev_file:
                        # ret.append(json.load(dev_file))
                        yield json.load(dev_file)
                        
                        
        except FileNotFoundError as fnf:
            self.logger.error(f'Get devices list {fnf}')
        except NotADirectoryError as nd:
            self.logger.error(f'Get devices list {nd}')
        
    def register_dev(self, device_info: Dict[str, Any]):
        self._check_device_info(device_info)
        try:
            driver_info: Dict[str,str] = device_info['driver']
            if not self.drivers.is_module_loaded(driver_info['module']):
                self.drivers.load_driver_module(driver_info['module'])
            driver = self.drivers.get_driver(driver_info['class'])
            print(driver)
        except KeyError as err:
            print(err)
        # drv = self.drivers.get_driver(dev["family"])
        # if drv:
        #     dev_instace = drv(dev['model'],
        #                       dev['sid'],
        #                       self.config.get(dev['sid']))
        #     if dev_instace:
        #         dev_instace.status.name = dev.get('name', '')
        #         dev_instace.status.place = dev.get('place', '')
        #         self._devices[dev['sid']] = dev_instace
        #     else:
        #         self._devices_fail_list.append(dev)
    
    def _check_device_info(self, device_info: Dict[str,str]) -> bool:
        return {'sid', 'driver', 'name', }.issubset(device_info)
            
    def get(self, key, ret=None):
        try:
            return self._devices[key]
        except KeyError:
            return ret
    
    # def get_devices_info_list(self) -> List[Dict[str,str]]:
    #     ret: List[Dict[str,str]] = list()
    #     for devitem in self._devices:
    #         dev = self.get(devitem)
    #         ret.append(dev.device_status())
    #     return ret
      
    def _unknown_device_family(self, data, *args):
        return None
    
    def __contains__(self, key: str):
        return key in self._devices
    
    def __getitem__(self, key: str):
        return self._devices[key]


