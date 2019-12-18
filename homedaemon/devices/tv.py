from .base import BaseDevice
from homedaemon.bravia import Bravia

class TvDevice:
    def __init__(self, data):
        pass


class Bravia(BaseDevice):
    def __init__(self, data, daemon):
        super(Bravia, self).__init__(data, daemon)
        self.ip = data.get('ip')
        self.mac = data.get('mac')
        self.tv = Bravia(self.ip, macaddres=self.mac)

    def write(self, cmd):
        data = cmd.get('data')
        if 'button' not in data:
            self.daemon.logger.error(f'wrong command {cmd}')
            return
        if data.get('button') == 'PowerOn':
            self.tv.power_on()
        elif self.tv.is_on():
            self.tv.send_command(data['button'])
        else:
            self.daemon.logger.warning('tv is off')
    
    def on(self):
        self.tv.power_on()
    
    def off(self):
        self.tv.power_off()
    
    @property
    def power(self):
        return self.tv.is_on()
