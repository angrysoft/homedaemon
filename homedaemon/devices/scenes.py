from .base import Dummy
import importlib

class SceneDevice:
    def __new__(cls, data, daemon):
        try:
            _scene = importlib.import_module(data.get('sid'))
            return _scene.Scene(data['sid'], daemon)
        except ModuleNotFoundError as err:
            daemon.logger.error(str(err))