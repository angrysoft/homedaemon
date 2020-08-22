import importlib
from os import DirEntry, scandir
from homedaemon.config import Config
from homedaemon.logger import Logger
import json
import asyncio
from typing import Iterator, List, Dict

class Drivers:
    devices_drivers: Dict[str, Driver] = dict()
    
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
    
    def register_devices(self, daemon) -> None:
        for dev in self.get_devices_list():
            self.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')} from {dev.get('place')}")
            # try:
            self.register_dev(dev, daemon)
            # except Exception as err:
                # self._devices_fail_list.append(dev)
                # self.logger.error(str(err))
            # daemon.loop.run_in_executor(None, self.register_dev, dev, daemon)
        daemon.loop.create_task(self._watch_devices_fail_list(daemon))
    
    async def _watch_devices_fail_list(self, daemon):
        while True:
            self.logger.debug(f"Device fail list : {self._devices_fail_list}")
            for dev in self._devices_fail_list:
                self.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')}")
                try:
                    self.register_dev(dev, daemon)
                except Exception as err:
                    self._devices_fail_list.append(dev)
                    self.logger.error(str(err))
            
            await asyncio.sleep(60)
        
    def get_devices_list(self):
        ret = []
        try:
            _dir: Iterator[DirEntry[str]] = scandir(path=self.config.get('devices_dir'))
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
            else:
                self._devices_fail_list.append(dev)
            
    def get(self, key, ret=None):
        try:
            return self._devices[key]
        except KeyError:
            return ret
    
    def get_devices_info_list(self) -> List[Dict[str,str]]:
        ret: List[Dict[str,str]] = list()
        for devitem in self._devices:
            dev = self.get(devitem)
            ret.append({'sid': dev.sid, 'model': dev.model,
                        'name': dev.name, 'place': dev.place,
                        'status': dev.device_status()})
        return ret
      
    def _unknown_device_family(self, data, *args):
        return None
    
    def __contains__(self, key: str):
        return key in self._devices
    
    def __getitem__(self, key: str):
        return self._devices[key]


