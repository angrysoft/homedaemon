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
            else:
                self.daemon.inputs['Arduino'].serial_write(self.get_rgb(_data))

    def report(self, data):
        if 'data' in data:
            data['data']['status'] = self._status(data['data'])
            if data['data']['status'] == 'off':
                data['data']['default'] = self.rgb_to_default()

        self.daemon.logger.info(str(data))
        self.daemon.notify_clients(json.dumps(data))
        self.update_dev_data(data.get('data'))

    @staticmethod
    def _status(data):
        rgb = (int(data.get('red', '0')) + int(data.get('green', '0')) + int(data.get('blue', '0'))) * \
              int(int(data.get('dim', '100')) / 100)
        if rgb > 0:
            return 'on'
        else:
            return 'off'

    def rgb_to_default(self):
        r = self.daemon.device_data[self.sid].get('red', 0)
        g = self.daemon.device_data[self.sid].get('green', 0)
        b = self.daemon.device_data[self.sid].get('blue', 0)
        d = self.daemon.device_data[self.sid].get('dim', 100)
        if int(r) + int(g) + int(b) == 0:
            r = '255'
            g = '255'
            b = '255'
        return {'red': r, 'green': g, 'blue': b, 'dim': d}

    def get_rgb(self, data):
        d = int(int(data.get('dim', '100')) / 100)
        r = int(data.get('red', '0')) * d
        g = int(data.get('green', '0')) * d
        b = int(data.get('blue', '0')) * d
        self.daemon.logger.info(f'F:{r}.{g}.{b}')
        return f'F.{r}.{g}.{b}'

    def off(self):
        if 'Arduino' in self.daemon.inputs:
            self.daemon.inputs['Arduino'].serial_write('F.0.0.0')

    def on(self):
        color = self.daemon.device_data[self.sid].get('default',
                                                      {'red': '255', 'green': '255', 'blue': '255', 'dim': '100'})
        if 'Arduino' in self.daemon.inputs:
            self.daemon.inputs['Arduino'].serial_write(self.get_rgb(color))

