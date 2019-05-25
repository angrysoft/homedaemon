import json


class Scene:
    def __init__(self, path):
        self.name = 'empty'
        self._load_scene_config(path)
        self.on = list()
        self.off = list()

    def _load_scene_config(self, path):
        try:
            with open(path, 'r') as jfscene:
                data = json.load(jfscene)
            self.name = data.get('name')
            self.on = data.get('on')
            self.off = data.get('off')
        except json.JSONDecodeError:
            pass

    def do(self, data):
        if 'data' in data:
            print('scene', data['data'].get('status'))

    def run_scene(self):
        pass


