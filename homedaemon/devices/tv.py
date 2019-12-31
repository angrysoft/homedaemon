from .base import BaseDevice, Dummy
from pytvremote import Bravia

class TvDevice:
    def __new__(cls, data, daemon):
        return {'bravia': BraviaTv}.get(data.get('model'), Dummy)(data, daemon)


class BraviaTv(BaseDevice):
    def __init__(self, data, daemon):
        super(BraviaTv, self).__init__(data, daemon)
        self.ip = data.get('ip')
        self.mac = data.get('mac')
        self.tv = Bravia(self.ip, macaddres=self.mac)

    def write(self, cmd):
        data = cmd.get('data')
        if 'power' in data:
            {'on': self.on, 'off': self.off}.get(data['power'], self.unknown_cmd)()
        elif data.get('button') == 'PowerOn':
            self.tv.on()
            self.get_tv_status()
        elif self.tv.power:
            self.tv.send_ircc(data['button'])
            # TODO: chekc if button is channel or src
            self.get_tv_status()
        else:
            self.daemon.logger.warning('tv is off')
    
    def unknown_cmd(self):
        self.daemon.logger.error(f'wrong command')    
    
    def get_tv_status(self):
        tvstatus = dict()
        if self.tv.power:
            tvstatus['status'] = 'on'
            tvstatus.update(self.tv.content_info())
        else:
            tvstatus['status'] = 'off'
                
        self.daemon.bus.emit_cmd({'cmd': 'report', 'sid': 'tv01',  'data': tvstatus})
        
    def on(self):
        self.tv.on()
    
    def off(self):
        self.tv.off()
    
    @property
    def power(self):
        return self.tv.power
