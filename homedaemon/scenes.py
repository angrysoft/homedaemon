import json
from threading import Thread


class Commands(Thread):
    def __init__(self, cmds, queue_put):
        super().__init__()
        self.cmds = cmds
        self.queue_put = queue_put

    def run(self):
        for c in self.cmds:
            cmd = c.get('cmd')
            if cmd == 'device':
                print('dev', c.get('args'), type(c.get('args')))
                self.queue_put(c.get('args'))


class Scene:
    def __init__(self, path, queue_put):
        self.name = 'empty'
        self.cmds = {'on': [], 'off': []}
        self._load_scene_config(path)
        self.status = None
        self.queue_put = queue_put

    def _load_scene_config(self, path):
        try:
            with open(path, 'r') as jfscene:
                data = json.load(jfscene)
            self.name = data.get('name')
            self.cmds['on'] = data.get('on')
            self.cmds['off'] = data.get('off')
        except json.JSONDecodeError:
            pass

    def do(self, data):
        if 'data' in data:
            Commands(self.cmds.get(data['data'].get('status'), []),
                     self.queue_put).start()







