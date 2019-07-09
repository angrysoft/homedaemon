from . import BaseDevice
from homedaemon.bravia import Bravia


class BraviaTv(BaseDevice):
    def __init__(self, data, daemon):
        super(BraviaTv, self).__init__(data, daemon)
        self.ip = data.get('ip')
        self.mac = data.get('mac')
        self.tv = Bravia(self.ip, macaddres=self.mac)

    def write(self, cmd):
        data = cmd.get('data')
        if 'button' not in data:
            print(cmd)
            return
        if data.get('button') == 'PowerOn':
            self.tv.power_on()
        elif self.tv.is_on():
            self.tv.send_command(data['button'])
        else:
            print('tv is off')
