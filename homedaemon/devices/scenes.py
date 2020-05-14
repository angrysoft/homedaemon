from .base import Dummy
import importlib
import sys
from homedaemon.config import Config

config = Config()
if config['scenes']:
    importlib.sys.path.append(config['scenes']['path'])

print(importlib.sys.path)

class Driver:
    def __new__(cls, data, daemon):
        try:
            _scene = importlib.import_module(data.get('sid'))
            return _scene.Scene(data['sid'], daemon)
        except ModuleNotFoundError as err:
            daemon.logger.error(str(err))