import json
from threading import Thread, Event
from datetime import datetime, time
from time import sleep

class SceneInterface:
    def __init__(self, sid, daemon):
        self.sid = sid
        self.daemon = daemon
        self.name = ''
        self.running = False
    
    def _runner(self, handler, *args):
        self.daemon.bus.emit(f'report.{self.sid}.status.on')
        self.running = True
        try:
            handler()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:
            self.daemon.bus.emit(f'report.{self.sid}.status.off')
            self.running = False
        # sc = Thread(name=self.name, target=handler, args=args)
        # sc.start()
    
    def sleep(self, s):
        sleep(s)
        
    def run_after(self, delay, callback, cancelable=False):
        pass

    def get_device(self, sid):
        return self.daemon.devices.get(sid)

    def store_device_state(self, *sids):
        pass
    
    def restore_devices_state(self, *sids):
        pass

class BaseScene(SceneInterface):
    def __init__(self, sid, daemon):
        super().__init__(sid, daemon)
        self.reversible = False
        self.daemon.bus.add_trigger(f'write.{self.sid}.status.on', self._runner, self.on)
        self.daemon.bus.add_trigger(f'write.{self.sid}.status.off',self._runner, self.off)
                    
    def _on(self):
        self.daemon.bus.emit(f'report{self.sid}.status.on')
        self.running = True
        try:
            self.on()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:
            if not self.reversible:
                self.daemon.bus.emit(f'report{self.sid}.status.off')
                
    def on(self):
        pass
    
    def _off(self):
        if not self.reversible or not self.running:
            return
        try:
            self.off()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:
            self.daemon.bus.emit(f'report{self.sid}.status.off')
            self.running = False
            
        
    def off(self):
        pass

    
class BaseAutomation(SceneInterface):
    def __init__(self, sid, daemon):
        super().__init__(sid, daemon)    
        
    def add_trigger(self, trigger, handler):
        self.daemon.bus.add_trigger(trigger, self._runner, handler)
    

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


