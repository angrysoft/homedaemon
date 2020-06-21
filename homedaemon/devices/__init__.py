import importlib
from pycouchdb import Server

class Devices:
    def __init__(self):
        self.drivers = Drivers()
        self._devices = dict()
        self._devices_fail_list =list()
    
    def register_devices(self, daemon):
        for dev in self.get_devices_list():
            daemon.logger.debug(f"Loading....{dev['sid']} : {dev.get('name')}")
            try:
                self.register_dev(dev, daemon)
            except Exception as err:
                daemon.logger.error(str(err))
            # daemon.loop.run_in_executor(None, self.register_dev, dev, daemon)
    
    def get_devices_list(self):
        self.db = Server()
        self.devicesdb = self.db['devices']
        return self.devicesdb.get_all_docs()
        
    def register_dev(self, dev, daemon):
        drv = self.drivers.get_driver(dev["family"])
        if drv:
            dev_instace = drv(dev, daemon)
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
