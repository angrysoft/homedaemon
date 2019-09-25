from . import BaseDevice

class Computer(BaseDevice):
    def __init__(self, data, daemon):
        super(Computer, self).__init__(data, daemon)
    
    def reboot(self):
        pass
    
    def daemon_restart(self):
        pass
    
    def daemon_reload(self):
        pass
    
    def reload_scenes(self):
        pass
    
    def reload_devices(self):
        pass