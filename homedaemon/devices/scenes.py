from .base import Dummy
import importlib
import sys
from homedaemon.config import Config

config = Config()
if config['scenes']:
    importlib.sys.path.append(config['scenes']['path'])
    

class Driver:
    def __new__(cls, model, sid, config, daemon):
        try:
            _scene = importlib.import_module(sid)
            return _scene.Scene(sid, daemon)
        except ModuleNotFoundError as err:
            daemon.logger.error(str(err))