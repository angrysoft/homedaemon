from .base import Dummy
import importlib
import sys
from homedaemon.config import Config
from homedaemon.logger import Logger

logger = Logger()

config = Config()
if config['scenes']:
    importlib.sys.path.append(config['scenes']['path'])
    

class Driver:
    def __new__(cls, model, sid, config):
        try:
            _scene = importlib.import_module(sid)
            return _scene.Scene(sid)
        except ModuleNotFoundError as err:
            logger.error(str(err))