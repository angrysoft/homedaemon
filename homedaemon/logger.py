from systemd.journal import JournalHandler
from sys import stdout
import logging


class Logger:
    _logger = None
    _debug = False
    _std = False
    
    def __new__(cls, debug=False, std=False):
        if Logger._logger is None:
            Logger._logger = logging.getLogger('homed')
            Logger._logger.addHandler(JournalHandler())
            if std:
                # TODO : std out enable / disable
                Logger._logger.addHandler(logging.StreamHandler(stdout))
            Logger._debug = debug
            if  debug:    
                 Logger._logger.setLevel(logging.DEBUG)
        return super(Logger, cls).__new__(cls)
    
    def debug(self, msg=None):
        if msg is not None and self._debug:
            self._logger.debug(f">>DEBUG<< {msg}")
    
    def info(self, msg=None):
        if msg is not None:
            self._logger.info(f">INFO< {msg}")
    
    def error(self, msg=None):
        if msg is not None:
            self._logger.error(f"!!ERROR!! {msg}")
    
    def warning(self, msg=None):
        if msg is not None:
            self._logger.warning(f"!WARNING! {msg}")
    
    # def __del__(self):
    #     self._logger.removeHandler(JournalHandler())
    #     if self._logger.hasHandlers():
    #         self._logger.removeHandler(logging.StreamHandler(stdout))
    #     Logger._logger = None
        
    
    