from . import BaseDevice


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
        self.daemon.inputs['arduiono'].serial_write(self.get_rgb(data))

    @staticmethod
    def get_rgb(data):
        d = int(data.get('dim', '100')) / 100
        r = int(data.get('red', '0')) * d
        g = int(data.get('green', '0')) * d
        b = int(data.get('blue', '0')) * d

        return f'F:{r}.{g}.{b}'

    def off(self):
        self.write({'red': 0, 'green': 0, 'blue': 0})

    def on(self):
        self.write(self.daemon.device_data.get('default',
                                               {'red': 255, 'green': 255, 'blue': 255}))

