import json
from threading import Thread
from datetime import datetime, time
from time import sleep


class BaseScene(Thread):
    name = ''
    automatic = True
    _triggers = []
    running = False

    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
    
    @property
    def triggers(self):
        return self._triggers
    
    @triggers.setter
    def triggers(self, value):
        self._triggers.append(Trigger(value, self))
        
    def do(self, cmd):
        if 'status' in cmd:
            sc = Thread(name=self.name, target={'on': self.on, 'off': self.off}.get(cmd['status'], self._unknown_cmd))
            self.running = True
            sc.start()
            # sc.join()
            self.running = False
        else:
            self.daemon.logger.error(f'{self.name}: missing status')
    
    def on(self):
        pass

    def off(self):
        pass

    def _unknown_cmd(self):
        self.daemon.logger.error(f'unknown status')

    def sleep(self, s):
        sleep(s)

    def get_device(self, sid):
        return self.daemon.workers.get(sid)


class Triggers:
    def __init__(self):
        self._triggers = dict()
    
    def register(self, trigger):
        if trigger is None:
            return
        elif not isinstance(trigger, Trigger):
            raise ValueError('arg need to by Trigger instance')
        if trigger.sid not in self._triggers:
            self._triggers[trigger.sid] = list()
        self._triggers[trigger.sid].append(trigger)

    def unregister(self, sid):
        if sid in self._triggers:
            del self._triggers[sid]

    def on_event(self, event):
        for trigger in self._triggers.get(event.get('sid'), []):
            if event.get('data', dict()).get(trigger.event) == trigger.value:
                trigger.pull()


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
    
    def pull(self):
        self._scene.do({'status': 'on'})


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


