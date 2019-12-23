import json
from threading import Thread
from datetime import datetime, time
from time import sleep


class BaseScene(Thread):
    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        self.name = ''
        self._automatic = True
        self._triggers = list()
        self.running = False
    
    @property
    def triggers(self):
        return self._triggers
    
    @triggers.setter
    def triggers(self, value):
        if self._automatic:
            trig = Trigger(value, self)
            self._triggers.append(trig)
            self.daemon.bus.on('report', trig.sid, trig.pull)
    
    @property
    def automatic(self):
        return self._automatic
    
    @autmatic.setter
    def automatic(self, value):
        self._automatic = value
        if value is False:
            self.daemon.bus.on('write', self.name, self.do)

    def do(self, cmd):
        if 'status' in cmd:
            sc = Thread(name=self.name, target={'on': self.on, 'off': self.off}.get(cmd['status'], self._unknown_cmd))
            self.running = True
            sc.start()
            # sc.join()
            self.running = False
        else:
            self.daemon.logger.error(f'{self.name}: missing status')
    
    def _runner(self, status):
        cmd = {'cmd': 'report', 'sid': self.name, 'data':{'status': status, 'running': True}}
        if status == 'on':
            self.running = True
            self.daemon.bus.emit('report', self.name, cmd)
            self.on()
        elif status == 'off':
            self.running
            
            
    def on(self):
        pass

    def off(self):
        pass

    def _unknown_cmd(self):
        self.daemon.logger.error(f'unknown status')

    def sleep(self, s):
        sleep(s)

    def get_device(self, sid):
        return self.daemon.devices.get(sid)


class Trigger:
    sid = ''
    event = ''
    value = ''
    def __init__(self, trigger, scene):
        if type(trigger) is str:
            _values = trigger.split('.')
            if len(_values) == 3:
                self.sid, self.event, self.value = _values
        self._scene = scene
    
    def pull(self, event):
        if event.get('data', dict()).get(self.event) == self.value:
            self._scene.do({'status': 'on'})
    
    def __repr__(self):
        return f'Trigger: {self.sid}.{self.event}.{self.value}'


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


