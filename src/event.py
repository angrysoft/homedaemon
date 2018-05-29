import json

class EventBase:
    def __init__(self):
        self._event = 'event'
        self.ctrl = None
        self.args = None
        self._type = ''

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._event

    def send(self, s):
        cmd = '{}\n'.format(s)
        self.ctrl.write(cmd.encode())

    def run(self, ctrl, args=None):
        self.ctrl = ctrl
        self.args = args
        self.start()

    def start(self):
        pass


class Button:
    def __init__(self, data):
        self.name = data.get('name')
        self.alias = data.get('alias')
        self.on = data.get('On')
        self.off = data.get('Off')


class Rf:
    def __init__(self, config='/etc/smarthouse/rf433.json'):
        self.buttons = list()
        with open(config) as jfile:
            data = json.load(jfile)
            for b in data:
                d = {'name': b}
                d.update(data[b])
                self.buttons.append(Button(d))

    def on(self, btn):
        for b in self.buttons:
            if b.name == btn or b.alias == btn:
                return 'W.{}'.format(b.on)

    def off(self, btn):
        for b in self.buttons:
            if b.name == btn or b.alias == btn:
                return 'W.{}'.format(b.off)

class RGB:
    def __init__(self):
        self._red = 0
        self._green = 0
        self._blue = 0
        self._dimmer = 0

    @property
    def red(self):
        ret = self._red * (self._dimmer / 255)
        if ret < 0:
            return 0
        else:
            return int(ret)

    @red.setter
    def red(self, val):
        self.isInt(val)
        self._red = val

    @property
    def green(self):
        ret = self._green * (self._dimmer / 255)
        if ret < 0:
            return 0
        else:
            return int(ret)

    @green.setter
    def green(self, val):
        self.isInt(val)
        self._green = val

    @property
    def blue(self):
        ret = self._blue * (self._dimmer / 255)
        if ret < 0:
            return 0
        else:
            return int(ret)

    @blue.setter
    def blue(self, val):
        self.isInt(val)
        self._blue = val

    @property
    def dimmer(self):
        return self._dimmer

    @red.setter
    def dimmer(self, val):
        self.isInt(val)
        self._dimmer = val

    def rgb(self, col):
        r, g, b = col.split('.')
        self.red = int(r)
        self.green = int(g)
        self.blue = int(b)

    def color(self):
        return 'F.{}.{}.{}'.format(self.red, self.green, self.blue)

    def isInt(self, v):
        if not type(v) == int:
            raise TypeError('expected integer')
        if v < 0 or v > 255:
            raise ValueError('rang 0 > 255')
        print(v)