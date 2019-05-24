import json


class Scene:
    def __init__(self, path):
        self.name = 'empty'

        try:
            with open(path, 'r') as jfscene:
                data = json.load(jfscene)
                self._load_scene_config(data)
        except json.JSONDecodeError:
            pass

    def _load_scene_config(self, data):
        self.name = data.get('name')
        print(data)

    def do(self, data):
        if data is 'on':
            pass
        elif data is 'off':
            pass

