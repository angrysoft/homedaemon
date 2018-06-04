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

    def rfcode(self, code):
        return 'W.{}'.format(code)