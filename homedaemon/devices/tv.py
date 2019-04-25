from . import BaseDevice
from homedaemon.bravia import Bravia


class BraviaTv(BaseDevice):
    def __init__(self, data):
        super(BraviaTv, self).__init__(data)
        self.ip = data.get('ip')
        self.mac = data.get('mac')

    def do(self, token, cmd):
        print(self.ip, self.mac)
        b = Bravia(self.ip, macaddres=self.mac)

        if 'button' not in cmd:
            return
        if cmd.get('button') == 'PowerOn':
            b.power_on()
        elif b.is_on():
            b.send_command(cmd['button'])
        else:
            print('tv is off')
