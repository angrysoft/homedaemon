
import asyncio
import functools
from datetime import datetime


class Bus:
    def __init__(self, loop):
        self._events = dict()
        self.loop = loop
        
    def on(self, event, _id, *handlers):
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
        event_list = self._events[event.get('cmd')].get(event.get('sid'), []).copy()
        event_list.extend(self._events[event.get('cmd')].get('*', []))
        
        for ev in event_list:
            if self.is_async(ev):
                task = asyncio.run_coroutine_threadsafe(ev(event), self.loop)
                print(f'{datetime.now()} async {ev.__name__} {ev}')
            else:
                print(f'{datetime.now()} sync {ev.__name__} {ev}')
                ev(event)
            
    def is_async(self, ev):
        if asyncio.iscoroutine(ev) or asyncio.iscoroutinefunction(ev):
            return True
        else:
            return False
    
    def emit(self, event_id, msg=None):
        print(f'debug: {event_id}, {msg}')
        for ev in self._events.get(event_id, []):
            ev(msg)

