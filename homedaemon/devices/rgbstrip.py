from . import BaseDevice
import json


class RgbStrip(BaseDevice):
    def __init__(self, data, daemon):
        super(RgbStrip, self).__init__(data, daemon)
        self.writeable = True
        self.short_id = data.get('short_id')
        self.name = data.get('name')
        self.cmds['off'] = self.off
        self.cmds['on'] = self.on

    def write(self, data):
        print('write',
              self.model,
              self.sid,
              self.short_id,
              data)
        if type(data) is not dict:
            raise ValueError('Data argument is not dict')
        if not self.writeable:
            raise PermissionError('Device is not writable')
        if 'Arduino' in self.daemon.inputs and 'data' in data:
            _data = data['data']
            if 'status' in _data:
                if _data['status'] == 'on':
                    self.on()
                elif _data['status'] == 'off':
                    self.off()
            elif 'set_bright' in _data:
                self.bright(_data)
            elif 'set_ct_abx' in _data:
                self.ct(_data)
            elif 'set_rgb' in _data:
                self.set_rgb(_data)
            else:
                self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(_data))

    def report(self, data):
        if 'data' in data:
            data['data']['status'] = self._status(data['data'])

        self.daemon.notify_clients(json.dumps(data))
        self.update_dev_data(data.get('data'))

    @staticmethod
    def _status(data):
        rgb = (int(data.get('red', '0')) + int(data.get('green', '0')) + int(data.get('blue', '0')))

        if rgb > 0 and data.get('bright') > 0:
            return 'on'
        else:
            return 'off'

    def get_rgb(self):
        r = self.daemon.device_data[self.sid].get('red', 0)
        g = self.daemon.device_data[self.sid].get('green', 0)
        b = self.daemon.device_data[self.sid].get('blue', 0)
        d = self.daemon.device_data[self.sid].get('bright', 100)
        return {'red': r, 'green': g, 'blue': b, 'bright': d}
    
    def set_default(self):
        rgb = self.get_rgb()
        if int(rgb['red']) + int(rgb['green']) + int(rgb['blue'] + int(rgb['bright'])) == 0:
            rgb['red'] = '255'
            rgb['green'] = '255'
            rgb['blue'] = '255'
            rgb['bright'] = '100'
        self.daemon.device_data[self.sid]['default'] = rgb
        

    def _rgb_to_send(self, data):
        return f"F.{data.get('red', '0')}.{data.get('green', '0')}.{data.get('blue', '0')}.{data.get('bright', '100')}"

    def off(self):
        if 'Arduino' in self.daemon.inputs:
            self.daemon.inputs['Arduino'].serial_write('F.0.0.0.0')

    def on(self):
        color = self.daemon.device_data[self.sid].get('default',
                                                      {'red': '255', 'green': '255', 'blue': '255', 'bright': '100'})
        if 'Arduino' in self.daemon.inputs:
            self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(color))

    def bright(self, data):
        if 'Arduino' in self.daemon.inputs:
            rgb = self.get_rgb()
            rgb['bright'] = data.get('set_bright')
            self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(rgb)
            
    def ct(self, data):
        print(data.get('ct'))
    
    def set_rgb(self, data):
        if 'bright' not in data:
            data['bright'] = self.daemon.device_data[self.sid].get('bright', 100)
        
        if 'Arduino' in self.daemon.inputs:
            self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(data.get('set_rgb')))


#
kelvin_table = {
    1700: (255, 121, 0),
    1800: (255, 126, 0),
    1900: (255, 131, 0),
    2000: (255, 138, 18),
    2100: (255, 142, 33),
    2200: (255, 147, 44),
    2300: (255, 152, 54),
    2400: (255, 157, 63),
    2500: (255, 161, 72),
    2600: (255, 165, 79),
    2700: (255, 169, 87),
    2800: (255, 173, 94),
    2900: (255, 177, 101),
    3000: (255, 180, 107),
    3100: (255, 184, 114),
    3200: (255, 187, 120),
    3300: (255, 190, 126),
    3400: (255, 193, 132),
    3500: (255, 196, 137),
    3600: (255, 199, 143),
    3700: (255, 201, 148),
    3800: (255, 204, 153),
    3900: (255, 206, 159),
    4000: (255, 209, 163),
    4100: (255, 211, 168),
    4200: (255, 213, 173),
    4300: (255, 215, 177),
    4400: (255, 217, 182),
    4500: (255, 219, 186),
    4600: (255, 221, 190),
    4700: (255, 223, 194),
    4800: (255, 225, 198),
    4900: (255, 227, 202),
    5000: (255, 228, 206),
    5100: (255, 230, 210),
    5200: (255, 232, 213),
    5300: (255, 233, 217),
    5400: (255, 235, 220),
    5500: (255, 236, 224),
    5600: (255, 238, 227),
    5700: (255, 239, 230),
    5800: (255, 240, 233),
    5900: (255, 242, 236),
    6000: (255, 243, 239),
    6100: (255, 244, 242),
    6200: (255, 245, 245),
    6300: (255, 246, 247),
    6400: (255, 248, 251),
    6500: (255, 249, 253)}