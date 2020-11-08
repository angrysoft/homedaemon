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
    def __init__(self) -> None:
        self.drivers_modules: Dict[str, object] = {}
    
    def is_module_loaded(self, driver_module:str) -> bool:
        return driver_module in self.drivers_modules

    def get_driver(self, driver_module:str, driver_class:str):
        if not hasattr(self.drivers_modules[driver_module], driver_class):
            print(f'class not found {driver_class}')
        return getattr(self.drivers_modules[driver_module], driver_class)

    def load_driver_module(self, driver_module:str) -> None:
        print(f'load {driver_module}')
        # try:
        drv_mod = importlib.import_module(driver_module)
        self.drivers_modules[driver_module] = drv_mod
        # except ModuleNotFoundError as err:
        #     print(f'module not fond {err}')
        
        
class Devices:
    _instance = object = None
    
    def __new__(cls):
        if Devices._instance is None:
            cls.drivers: Drivers = Drivers()
            cls._devices: Dict[str, Drivers] = dict()
            cls._devices_fail_list: List[Dict[str,str]] = list()
            cls.config = Config()
            cls.logger = Logger()
            Devices._instance = object.__new__(cls)
        return cls._instance
    
    def register_devices(self) -> None:
        for dev in self.get_devices_info_list():
            self.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')} from {dev.get('place')}")
            self.register_dev(dev)
        
        print(self.drivers.drivers_modules)

        
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
        if self._check_device_info(device_info):    
            driver_info: Dict[str,str] = device_info['driver']
            if not self.drivers.is_module_loaded(driver_info['module']):
                self.drivers.load_driver_module(driver_info['module'])
            driver = self.drivers.get_driver(driver_info['module'], driver_info['class'])
            if 'gateway' in driver_info:
                gateway  = self._get_gateway(driver_info['gateway'])
                # add to args 
            
            # init dev with args
            # set dev name , place 
    
    def _check_device_info(self, device_info: Dict[str,str]) -> bool:
        # TODO: check value is not empty
        return {'sid', 'driver', 'name', 'place'}.issubset(device_info)
    
    def _get_gateway(self, sid:str):
        pass
    
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


