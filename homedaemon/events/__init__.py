from threading import RLock, Thread
from os import path, listdir


class EventBase:
    def __init__(self, daemon):
        self._event = 'event'
        self._type = 'event'
        self.daemon = daemon
        self.lock = RLock()

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._event

    def do(self, data):
        pass

    def update_dev_data(self, data):
        with self.lock:
            sid = data.get('sid')
            info = data.get('data')
            if sid and info:
                doc = self.daemon.device_data.get(sid)
                if doc:
                    doc.update(info)
                    self.daemon.device_data.save(doc)


# class SceneBase(Thread):
#     def __init__(self, daemon):
#         super(SceneBase, self).__init__()
#         self.lock = RLock()
#         self.daemon = daemon
#         self._scene = 'event'
#         self._type = 'scene'
#         self.data = None
#
#     def _load_scenes(self):
#         scene_dir =  self.daemon.config.get('scene_dir')
#         if path.exists(scene_dir):
#             pass
#
#     @property
#     def type(self):
#         return self._type
#
#     @property
#     def name(self):
#         return self._scene
#
#     def run(self, data):
#         pass
#
#     def do(self, data):
#         self.data = data
#         self.start()
