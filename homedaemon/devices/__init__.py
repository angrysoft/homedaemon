from __future__ import annotations
import importlib
from os import DirEntry, scandir
from homedaemon.config import Config
from homedaemon.logger import Logger
import json
from typing import Generator, Iterator, List, Dict

class DriverInterface:
    pass

class Drivers:
    devices_drivers: Dict[str, DriverInterface] = dict()
    
    def get_driver(self, device_family:str):
        self._register_driver(device_family)
        if device_family in self.devices_drivers:
            return self.devices_drivers[device_family]
        else:
            return None
    
    def _register_driver(self, dev_family:str) -> None:
        if not dev_family in self.devices_drivers:
            try:
                drv_mod = importlib.import_module(f'homedaemon.devices.{dev_family}')
                self.devices_drivers[dev_family] = drv_mod.Driver
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

        
    def get_devices_info_list(self) -> Generator[Dict[str,str], None, None]:
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
        
    def register_dev(self, device_info: Dict[str,str]):
        self._check_device_info(device_info)
        try:
            driver_info = device_info['driver']
            if not self.drivers.is_module_loaded(driver_info['']):
                self.drivers.load_driver_module(dev['driver'])
            driver = self.drivers.get_driver()
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


