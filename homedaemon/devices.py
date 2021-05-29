from __future__ import annotations
import importlib
from os import DirEntry, scandir
from homedaemon.config import Config
from homedaemon.logger import Logger
from homedaemon.bus import Bus
import json
from typing import Generator, Iterator, Dict, Any, Optional

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
        try:
            drv_mod = importlib.import_module(driver_module)
            self.drivers_modules[driver_module] = drv_mod
        except ModuleNotFoundError as err:
            print(f'module not fond {err}')

class Devices:
    _instance = object = None
    
    def __new__(cls):
        if Devices._instance is None:
            # cls._devices: Dict[str, Drivers] = {}
            Devices._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self._devices: Dict[str, Drivers] = {}
    
    def add(self, sid:str, device_instance: Any) -> None:
        self._devices[sid] = device_instance
    
    def remove(self, sid:str):
        if sid in self._devices:
            del self._devices[sid]
    
    def get(self, key:str, ret: Optional[Any]=None):
        try:
            return self._devices[key]
        except KeyError:
            return ret
    
    def __contains__(self, key: str):
        return key in self._devices
    
    def __getitem__(self, key: str):
        return self._devices[key]
    
        
class DevicesManager:
    def __init__(self):
        self.drivers: Drivers = Drivers()
        self._devices: Devices = Devices()
        self._gateways: Dict[str, Drivers] = {}
        self._gateways_info_list: Dict[str,Dict[str,Any]] = {}
        self._devices_info_list: Dict[str,Dict[str,Any]] = {}
        self._scenes_info_list: Dict[str,Dict[str,Any]] = {}
        self._devices_offline: Dict[str,Dict[str,Any]] = {}
        self._devices
        self.config: Config = Config()
        self.logger = Logger()
        self.bus = Bus()
        
        if self.config['scenes']:
            importlib.sys.path.append(self.config['scenes']['path'])
    
    def register_devices(self) -> None:
        self.load_devices_info()
        while self._devices_info_list:
            sid, device_info = self._devices_info_list.popitem()
            self.logger.debug(f"Loading..{len(self._devices_info_list)}..{sid} : {device_info.get('name')} from {device_info.get('place')}")
            try:
                self.register_dev(sid, device_info)
            except Exception as err:
                self._devices_offline[sid] = device_info
                self.logger.error( str(err) )
        
        while self._scenes_info_list:
            sid, device_info = self._scenes_info_list.popitem()
            self.logger.debug(f"Loading..{len(self._scenes_info_list)}..{sid} : {device_info.get('name')} from {device_info.get('place')}")
            self.register_scene(sid, device_info)
        
    def load_devices_info(self) -> None:
        try:
            for _file in scandir(path=self.config.get('devices_dir')):
                if _file.is_file and _file.name.endswith('.json'):
                    with open(_file.path) as dev_file:
                        # TODO load_device_info if is not proper skip device
                        device_info = json.load(dev_file)
                        if device_info.get('type', '') == 'gateway':
                            self._gateways_info_list[device_info['sid']] = device_info
                        elif device_info.get('type', '') == 'scene':
                            self._scenes_info_list[device_info['sid']] = device_info   
                        elif self._check_device_info(device_info):
                            self._devices_info_list[device_info['sid']] = device_info
        except FileNotFoundError as fnf:
            self.logger.error(f'Get devices list {fnf}')
        except NotADirectoryError as nd:
            self.logger.error(f'Get devices list {nd}')
        
    def register_dev(self, sid:str, device_info: Dict[str, Any]) -> None:
            
            driver_info: Dict[str,str] = device_info['driver']
            if not self.drivers.is_module_loaded(driver_info['module']):
                self.drivers.load_driver_module(driver_info['module'])
            
            device_info['args']['sid'] = sid
            
            if 'gateway' in driver_info:
                device_info['args']['gateway'] = self.get_gateway(driver_info['gateway'])
            
            driver = self.drivers.get_driver(driver_info['module'], driver_info['class'])
            
            dev = driver(**device_info['args'])
            dev.status.name = device_info['name']
            dev.status.place = device_info['place']
            dev.watcher.add_report_handler(self.bus.emit_cmd)
            self.bus.add_trigger(f'execute.{sid}.*.*', dev.execute)
            self._devices.add(sid, dev)
            device_status = dev.get_device_status()
            device_status['cmd'] = 'init_device'
            self.bus.emit(f'homed.device.init.{sid}', device_status)
    
    def get_gateway(self, gateway:str):
        if gateway not in self._gateways:
            self.register_gateway(gateway)
        return self._gateways[gateway]
    
    def register_gateway(self, gateway_sid:str):
        _gateway_info = self._gateways_info_list.pop(gateway_sid)
        driver_info: Dict[str,str] = _gateway_info['driver']
        if not self.drivers.is_module_loaded(driver_info['module']):
            self.drivers.load_driver_module(driver_info['module'])
        driver = self.drivers.get_driver(driver_info['module'], driver_info['class'])
        dev = driver(**_gateway_info['args'])
        self._gateways[_gateway_info['sid']] = dev

    def register_scene(self, sid:str, device_info: Dict[str, Any]):
        try:
            _scene_module = importlib.import_module(sid)
            _scene = _scene_module.Scene(sid)
            self._devices.add(sid, _scene)
            scene_status = _scene.device_status()
            scene_status['cmd'] = 'init_device'
            self.bus.emit(f'homed.device.init.{sid}', scene_status)
        except ModuleNotFoundError as err:
            self.logger.error(str(err))
    
    def _check_device_info(self, device_info: Dict[str,str]) -> bool:
        # TODO: check value is not empty
        return {'sid', 'driver', 'name', 'place', 'args'}.issubset(device_info)      
