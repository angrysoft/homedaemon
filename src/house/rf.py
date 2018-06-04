import json


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

    @staticmethod
    def code(val):
        return 'W.{}'.format(val)
