
import asyncio
import functools
from datetime import datetime
# from threading import current_thread


class Bus:
    def __init__(self, loop):
        self._events = dict()
        self.loop = loop
        self.running = []
        self._triggers = dict()
    
    def add_trigger(self, trigger:str, action) -> None:
        """report.12331313133.status.off
           report.342343243242.status.motion
        """
        pass
    
    def del_trigger(self):
        pass
    
    def emit(self):
        pass
        
    def on(self, event, _id, *handlers):
        # who what arg
        """ Register event"""
        if event not in self._events:
            self._events[event] = dict()
        if _id not in self._events[event]:
            self._events[event][_id] = list()
        for handler in handlers:
            self._events[event][_id].append(handler)
    
    def off(self, event, _id, handler):
        """ Unregister event"""
        _event = f'{event}.{_id}'
        if _event in self._events:
            self._events[_event] = list()
    
    def emit_cmd(self, event):
        if event.get('cmd') not in self._events:
            return
        
        event_list = self._events[event.get('cmd')].get(event.get('sid'), []).copy()
        event_list.extend(self._events[event.get('cmd')].get('*', []))
        
        for ev in event_list:
            # print(ev, current_thread())
            if self.is_async(ev):
                task = asyncio.run_coroutine_threadsafe(ev(event), self.loop)
                # print(f'async {ev.__name__} {event}')
            else:
                # print(f'sync {ev.__name__} {event}')
                # self.loop.call_soon(ev, event)
                ev(event)
            
    def is_async(self, ev):
        if asyncio.iscoroutine(ev) or asyncio.iscoroutinefunction(ev):
            return True
        else:
            return False

class Trigger:
    cmd = ''
    sid = ''
    event = ''
    value = ''
    def __init__(self, trigger, *actions):
        if type(trigger) is str:
            _values = trigger.split('.')
            if len(_values) == 4:
                self.cmd,self.sid, self.event, self.value = _values
        self._actions = actions
    
    def pull(self, event):
        if event.get('data', dict()).get(self.event) == self.value:
            self._scene.do({'data':{'status': 'on'}})
    
    def __repr__(self):
        return f'Trigger: {self.sid}.{self.event}.{self.value}'
    
    

if __name__ == "__main__":
    pass