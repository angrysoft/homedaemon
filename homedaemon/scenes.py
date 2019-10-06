import json
from threading import Thread
from datetime import datetime, time
from time import sleep


class BaseScene(Thread):
    name = ''
    automatic = True

    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        
    def do(self, cmd):
        if 'status' in cmd:
            self.cmd = cmd['status']
            self.start()
        else:
            self.daemon.logger.error(f'{self.name}: missing status')
    
    def run(self):
        {'on': self.on,
         'off': self.off}.get(self.cmd, self._unknown_cmd)()
    
    def on(self):
        pass

    def off(self):
        pass

    def _unknown_cmd(self):
        self.daemon.logger.error(f'unknown status {self.cmd}')

    def sleep(self, s):
        sleep(s)

    def get_device(self, sid):
        return self.daemon.workers.get(sid)


class TimeCheck:
    def __init__(self, operator, value1, value2=None):
        self._now = datetime.now().time()
        self._value1 = time(*[int(i) for i in value1.split(':')])
        if value2:
            self._value2 = time(*[int(i) for i in value2.split(':')])
        self.status = {'==': self.eq,
                       '>': self.gt,
                       '<': self.lt,
                       '<>':self.between}.get(operator)()

    def eq(self):
        return self._now == self._value1

    def gt(self):
        return self._now > self._value1

    def lt(self):
        return self._now < self._value1
    
    def between(self):
        _range = TimeRange(self._value1, self._value2)
        return self._now in _range
         
class TimeRange:
    """TimeRange"""
    def __init__(self, _from, _to):
        self._from = _from
        self._to = _to
    
    def __contains__(self, value):
        if value > self._to:
            return self._from <= value >= self._to
        elif value < self._to:
            return self._from >= value <= self._to


