import importlib
from homedaemon.config import Config
from homedaemon.logger import Logger

logger = Logger()

config = Config()
if config['scenes']:
    importlib.sys.path.append(config['scenes']['path'])
    

class SceneDriver:
    def __new__(cls, sid:str) -> object:
        try:
            _scene = importlib.import_module(sid)
            return _scene.Scene(sid)
        except ModuleNotFoundError as err:
            logger.error(str(err))