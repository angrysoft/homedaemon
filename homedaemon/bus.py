
import asyncio
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
        awitable = list()
        event_list = self._events[event.get('cmd')].get(event.get('sid'), [])
        event_list.extend(self._events[event.get('cmd')].get('*', []))
        
        for ev in event_list:
            if self.is_async(ev):
                # asyncio.run_coroutine_threadsafe(ev(event), self.loop)
                self.loop.run_until_complete(ev(event))
                print(f'{datetime.now()} async {ev.__name__} {event}')
            else:
                print(f'{datetime.now()} sync {ev.__name__} {event}')
                ev(event)
            
        # self._event(awitable)
    def is_async(self, ev):
        if asyncio.iscoroutine(ev) or asyncio.iscoroutinefunction(ev):
            return True
        else:
            return False
            
    def _event(self, ev):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            
        try:
            loop.run_until_complete(ev)
        finally:
            loop.stop()
    
    def emit(self, event_id, msg=None):
        print(f'debug: {event_id}, {msg}')
        for ev in self._events.get(event_id, []):
            ev(msg)
    


def print_msg1(m):
    print(f'msg 1 : {m}')


def print_msg2(m):
    print(f'msg 2 : {m}')


if __name__ == "__main__":
    b = Bus()
    b.on('report', print_msg1)
    b.on('report', print_msg2)
    b.emit('report', 'dupa blada')
