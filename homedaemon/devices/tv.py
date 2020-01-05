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

    def write(self, data):
        _data = data.get('data')
        c, v = _data.popitem()
        {'power' : self.set_power,
         'button': self.button}.get(c, self.unknown)(v)
    
    def set_power(self, status):
        {'on': self.on, 'off': self.off}.get(status, self.unknown)()
    
    def unknown(self, value=''):
        self.daemon.logger.error(f'unknown parametr {value}')
        
    def button(self ,btnname):    
        if btnname == 'PowerOn':
            self.tv.on()
        elif self.tv.power:
            self.tv.send_ircc(btnname)
            # TODO: chekc if button is channel or src
            if btnname in ['ChannelUp', 'ChannelDown', 'Input',
                           'Num0', 'Num1', 'Num2', 'Num3', 'Num4',
                           'Num5','Num6', 'Num7', 'Num8', 'Num9']:
                self.get_tv_status()
        else:
            self.daemon.logger.warning('tv is off')  
    
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
