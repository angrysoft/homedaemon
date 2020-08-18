from threading import Thread, Event
from datetime import datetime, time
from time import sleep
from typing import Dict, Any, List, Set, Callable


class SceneInterface:
    def __init__(self, sid:str, daemon):
        self.sid = sid
        self.daemon = daemon
        self.name = ''
        self.model = ''
        self.place = ''
        self.running: Set[Callable[[], None]] = set()
    
    def _runner(self, handler: Callable[[], None], *args) -> None:
        self.daemon.logger.debug(f'Scene {self.name} running list {self.running} {handler}')
        if handler in self.running:
            self.daemon.logger.warning(f'Scene {self.name}: {handler.__name__} allready started')
            return
        else:
            self.running.add(handler)
        self.daemon.bus.emit(f'report.{self.sid}.status.on', f'Scene {self.name}: {handler.__name__} start')
        
        try:
            handler()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:    
            self.daemon.bus.emit(f'report.{self.sid}.status.off', f'Scene {self.name}: {handler.__name__} end')
            self.running.remove(handler)
    
    def sleep(self, s:int):
        sleep(s)

    def get_device(self, sid:str):
        return self.daemon.devices.get(sid)

    def store_device_state(self, *sids):
        pass
    
    def restore_devices_state(self, *sids):
        pass
    
    def device_status(self) -> Dict[str,Any]:
        if self.running:
            events :List[Callable[[], None]] = [x.__name__ for x in self.running]
            return {'status': 'on', 'events': events}
        return {'status': 'off'}
    
    def now(self):
        """Retrun time now"""
        return datetime.now().time()
    

class BaseScene(SceneInterface):
    def __init__(self, sid:str, daemon):
        super().__init__(sid, daemon)
        self.reversible = False
        self.model = 'scene'
        self.daemon.bus.add_trigger(f'write.{self.sid}.status.on', self._on, self.on)
        self.daemon.bus.add_trigger(f'write.{self.sid}.status.off',self._off, self.off)
                    
    def _on(self):
        if self.on in self.running:
            self.daemon.logger.warning(f'Scene {self.name} allready started')
        else:
            self.running.add(self.on)
        self.daemon.bus.emit(f'report{self.sid}.status.on', f'Scene {self.name}: on')
        try:
            self.on()
            # sc = Thread(name=self.name, target=self.on)
            # sc.start()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:
            if not self.reversible:
                self.daemon.bus.emit(f'report{self.sid}.status.off', f'Scene {self.name}: off')
                
    def on(self):
        pass
    
    def _off(self):
        if not self.reversible or not self.on in self.running:
            return
        try:
            self.off()
            # sc = Thread(name=self.name, target=self.off)
            # sc.start()
        except Exception as err:
            self.daemon.logger.error(f'scene running error {self.name} {err}')
        finally:
            self.daemon.bus.emit(f'report{self.sid}.status.off', f'Scene {self.name}: off')
            self.running = False
            
    def off(self):
        pass

    
class BaseAutomation(SceneInterface):
    def __init__(self, sid:str, daemon):
        super().__init__(sid, daemon)    
        self.model = 'automation'
        
    def add_trigger(self, trigger:str, handler:Callable[[], None]) -> None:
        self.daemon.bus.add_trigger(trigger, self._runner, handler)


class RunAfter:
    def __init__(self, delay, callback, *args):
        self.delay = delay
        self.callback = callback
        self.args = args
        self.ev = Event()
        self._is_waiting = False
                
    def wait(self):
        Thread(target=self._wait, daemon=True).start()
    
    def _wait(self):
        self.ev.clear()
        self._is_waiting = True
        if not self.ev.wait(timeout=self.delay):
            if self.args:
                self.callback(*self.args)
            else:
                self.callback()
        else:
            print('canceled')
            
    @property
    def is_waiting(self):
        return self._is_waiting
    
    def cancel(self):
        self.ev.set()
        self._is_waiting = False

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


class Time(time):
    def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, time_str=None):
        if time_str:
            return time.__new__(cls, *[int(i) for i in time_str.split(':')])
        else:
           return time.__new__(cls, hour, minute, second, microsecond)
    
    def __add__(self, in_time):
        return self.to_sec() + in_time.to_sec()
    
    def __sub__(self, in_time):
        if self < in_time:
            raise ValueError
        return self.to_sec() - in_time.to_sec()
    
    def to_sec(self):
        return self.microsecond/1000000 + self.second + self.minute * 60 + self.hour * 3600