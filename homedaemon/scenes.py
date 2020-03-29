import json
from threading import Thread, Event
from datetime import datetime, time
from time import sleep

class Scenes:
    def __init__(self):
        self._scenes = dict()
    
    def load(self, scene):
        pass
    
    

class BaseScene(Thread):
    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        self.name = ''
        self._automatic = True
        self.reversible = False
        self.running = False
        self.place = ''
    
    def add_trigger(self, trigger, handler):
        daemon.bus.add_trigger(trigger, handler)
    
    @property
    def automatic(self):
        return self._automatic
    
    @automatic.setter
    def automatic(self, value):
        self._automatic = value
        if value is False:
            self.daemon.bus.on('write', self.name, self.do)

    def do(self, cmd):
        data = cmd.get('data', {})
        sc = Thread(name=self.name, target=self._runner, args=(data.get('status'),))
        sc.start()
    
    def _runner(self, status):
        if self.running:
            self.daemon.logger.warning(f'scene {self.name} is already running')
            return
        cmd = {'cmd': 'scene', 'sid': self.name, 'data':{'status': status, 'running': True}}
        self.running = True
        self.daemon.bus.emit_cmd(cmd)
        try:
            {'on': self.on, 'off': self.off}.get(status, self._unknown_cmd)()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:
            self.running = False
            cmd['data']['running'] = False
            self.daemon.bus.emit_cmd(cmd)
        self.daemon.logger.debug(f'debug : scene {self.name} {status}')
                    
    def on(self):
        pass

    def off(self):
        pass

    def _unknown_cmd(self):
        self.daemon.logger.error(f'unknown status')

    def sleep(self, s):
        sleep(s)
        
    def run_after(self, delay, callback, cancelable=False):
        pass

    def get_device(self, sid):
        return self.daemon.devices.get(sid)
    
    def store_device_state(self, *sids):
        pass
        # self.daemon.scenesdb[self.name]['state'] = {}
        # for sid in sids:
        #     self.daemon.scenesdb[self.name]['state'][sid] = self.daemon.device_data[sid]
    
    def restore_devices_state(self, *sids):
        pass


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


