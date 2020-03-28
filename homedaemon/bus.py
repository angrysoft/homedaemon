
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
    def __init__(self, trigger):
        if type(trigger) is str:
            _values = trigger.split('.')
            if len(_values) == 4:
                self.cmd,self.sid, self.event, self.value = _values
    
    def __repr__(self):
        return f'Trigger: {self.cmd}.{self.sid}.{self.event}.{self.value}'
    

class TriggerDict:
    def __init__(self):
        self._data = dict()
    
    def setdefault(self, key, value):
        return self._data.setdefault(key, value)
    
    def getkeys(self, keyname:str) -> list:
        ret = list()
        if keyname in self._data:
            ret.append(self._data[keyname])
        if '*' in self._data:
            ret.append(self._data['*'])
        return ret
    
    def get_path_key(self, *keys):
        # print('keys', keys)
        try:
            ret = list()
            _keys = list(keys)
            k = _keys.pop(0)
            for i in self.getkeys(k):
                # print('i', i)
                if isinstance(i, TriggerDict):
                    ret.extend(i.get_path_key(*_keys))
                else:
                    ret.extend(i)
        except IndexError:
            pass
        return ret
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __repr__(self):
        return self._data.__repr__()

class Triggers:
    def __init__(self):
        self._triggers = TriggerDict()
    
    def add_trigger(self, trigger:Trigger, handler, *args) -> None:
        cmd = self._triggers.setdefault(trigger.cmd, TriggerDict())
        sid = cmd.setdefault(trigger.sid, TriggerDict())
        event = sid.setdefault(trigger.event, TriggerDict())
        value = event.setdefault(trigger.value, [])
        value.append((handler, args))
    
    def get_handlers(self, trigger:Trigger) -> list:
        try:
            return self._triggers.get_path_key(trigger.cmd, trigger.sid, trigger.event, trigger.value)
        except KeyError:
            return []
        
    def __repr__(self):
        return str(self._triggers)
        
            
        


if __name__ == "__main__":
    tr = Triggers()
    t = Trigger('report.12331313133.status.off')
    t0 = Trigger('report.*.status.off')
    t1 = Trigger('report.342343243242.status.motion')
    t2 = Trigger('connect.*.tcpclient.connected')
    t3 = Trigger('report.*.*.*')
    # print(t, t1, t2)
    tr.add_trigger(t, print, 'dupa')
    tr.add_trigger(t0, print, 'dupa blada')
    tr.add_trigger(t1, dir)
    tr.add_trigger(t2, print,  'tu cie ', 'mam ', ':}')
    tr.add_trigger(t3, print)
    # print(tr)
    for h, a in tr.get_handlers(Trigger('report.12331313133.status.off')):
        h(*a)
    print(tr.get_handlers(Trigger('report.3244242.status.off')))