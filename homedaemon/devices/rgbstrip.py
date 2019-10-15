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
        # https://andi-siess.de/rgb-to-color-temperature/
        self.kelvin_table = {'1700': {'red': '255', 'green': '121', 'blue': '0'},
                             '1800': {'red': '255', 'green': '126', 'blue': '0'},
                             '1900': {'red': '255', 'green': '131', 'blue': '0'},
                             '2000': {'red': '255', 'green': '138', 'blue': '18'},
                             '2100': {'red': '255', 'green': '142', 'blue': '33'},
                             '2200': {'red': '255', 'green': '147', 'blue': '44'},
                             '2300': {'red': '255', 'green': '152', 'blue': '54'},
                             '2400': {'red': '255', 'green': '157', 'blue': '63'},
                             '2500': {'red': '255', 'green': '161', 'blue': '72'},
                             '2600': {'red': '255', 'green': '165', 'blue': '79'},
                             '2700': {'red': '255', 'green': '169', 'blue': '87'},
                             '2800': {'red': '255', 'green': '173', 'blue': '94'},
                             '2900': {'red': '255', 'green': '177', 'blue': '101'},
                             '3000': {'red': '255', 'green': '180', 'blue': '107'},
                             '3100': {'red': '255', 'green': '184', 'blue': '114'},
                             '3200': {'red': '255', 'green': '187', 'blue': '120'},
                             '3300': {'red': '255', 'green': '190', 'blue': '126'},
                             '3400': {'red': '255', 'green': '193', 'blue': '132'},
                             '3500': {'red': '255', 'green': '196', 'blue': '137'},
                             '3600': {'red': '255', 'green': '199', 'blue': '143'},
                             '3700': {'red': '255', 'green': '201', 'blue': '148'},
                             '3800': {'red': '255', 'green': '204', 'blue': '153'},
                             '3900': {'red': '255', 'green': '206', 'blue': '159'},
                             '4000': {'red': '255', 'green': '209', 'blue': '163'},
                             '4100': {'red': '255', 'green': '211', 'blue': '168'},
                             '4200': {'red': '255', 'green': '213', 'blue': '173'},
                             '4300': {'red': '255', 'green': '215', 'blue': '177'},
                             '4400': {'red': '255', 'green': '217', 'blue': '182'},
                             '4500': {'red': '255', 'green': '219', 'blue': '186'},
                             '4600': {'red': '255', 'green': '221', 'blue': '190'},
                             '4700': {'red': '255', 'green': '223', 'blue': '194'},
                             '4800': {'red': '255', 'green': '225', 'blue': '198'},
                             '4900': {'red': '255', 'green': '227', 'blue': '202'},
                             '5000': {'red': '255', 'green': '228', 'blue': '206'},
                             '5100': {'red': '255', 'green': '230', 'blue': '210'},
                             '5200': {'red': '255', 'green': '232', 'blue': '213'},
                             '5300': {'red': '255', 'green': '233', 'blue': '217'},
                             '5400': {'red': '255', 'green': '235', 'blue': '220'},
                             '5500': {'red': '255', 'green': '236', 'blue': '224'},
                             '5600': {'red': '255', 'green': '238', 'blue': '227'},
                             '5700': {'red': '255', 'green': '239', 'blue': '230'},
                             '5800': {'red': '255', 'green': '240', 'blue': '233'},
                             '5900': {'red': '255', 'green': '242', 'blue': '236'},
                             '6000': {'red': '255', 'green': '243', 'blue': '239'},
                             '6100': {'red': '255', 'green': '244', 'blue': '242'},
                             '6200': {'red': '255', 'green': '245', 'blue': '245'},
                             '6300': {'red': '255', 'green': '246', 'blue': '247'},
                             '6400': {'red': '255', 'green': '248', 'blue': '251'},
                             '6500': {'red': '255', 'green': '249', 'blue': '253'}}

    def write(self, data):
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
            self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(rgb))
            
    def ct(self, data):
        rgb = self.kelvin_table.get(data.get('set_ct_abx'))
        self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(rgb))
    
    def set_rgb(self, data):
        if 'bright' not in data:
            data['bright'] = self.daemon.device_data[self.sid].get('bright', 100)
        
        if 'Arduino' in self.daemon.inputs:
            self.daemon.inputs['Arduino'].serial_write(self._rgb_to_send(data.get('set_rgb')))


