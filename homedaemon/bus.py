
import asyncio
import functools
from datetime import datetime
from threading import current_thread

class Trigger:
    def __init__(self, trigger):
        if type(trigger) is str:
            _values = trigger.split('.', 4)
            if len(_values) == 4:
                self.cmd,self.sid, self.event, self.value = _values
        elif type(trigger) is dict:
            self.cmd = trigger['cmd']
            self.sid = trigger['sid']
            _data = trigger['data'].copy()
            self.event, self.value = _data.popitem()
    
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
        try:
            ret = list()
            _keys = list(keys)
            k = _keys.pop(0)
            for i in self.getkeys(k):
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

class Bus:
    def __init__(self, loop):
        self._events = dict()
        self.loop = loop
        self.running = []
        self._triggers = TriggerDict()
    
    def add_trigger(self, trigger:str, handler, *args) -> None:
        _trigger = Trigger(trigger)
        cmd = self._triggers.setdefault(_trigger.cmd, TriggerDict())
        sid = cmd.setdefault(_trigger.sid, TriggerDict())
        event = sid.setdefault(_trigger.event, TriggerDict())
        value = event.setdefault(_trigger.value, [])
        value.append((handler, args))
    
    def get_handlers(self, trigger:Trigger) -> list:
        try:
            return self._triggers.get_path_key(trigger.cmd, trigger.sid, trigger.event, trigger.value)
        except KeyError:
            return []
    
    def del_trigger(self, trigger:Trigger):
        pass
    
    def emit(self, event:str, *payload):
        trigger = Trigger(event)
        print(current_thread(), trigger, payload)
        for handler, args in self.get_handlers(trigger):
            if self.is_async(handler):
                if payload:
                    task = asyncio.run_coroutine_threadsafe(handler(*payload), self.loop)
                else:
                    task = asyncio.run_coroutine_threadsafe(handler(), self.loop)
            else:
                handler_with_args = list()
                handler_with_args.append(handler)
                handler_with_args.extend(args)
                handler_with_args.extend(payload)
                # handler()
                self.loop.run_in_executor(None, *handler_with_args)
    
    def emit_cmd(self, event):
        #TODO problem jak jest wieceje elementów w data
        self.emit(event, event)
            
    def is_async(self, ev):
        if asyncio.iscoroutine(ev) or asyncio.iscoroutinefunction(ev):
            return True
        else:
            return False


    

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
    def print_hand(a,b):
        print(a,b)
    tr = Triggers()
    t = Trigger('report.12331313133.status.off')
    t0 = Trigger('report.*.status.off')
    t1 = Trigger('report.342343243242.status.motion')
    t2 = Trigger('connect.*.tcpclient.connected')
    t3 = Trigger('report.*.*.*')
    # print(t, t1, t2)
    tr.add_trigger(t, 't1 fucn 1', 't1 arg 1', 't1 arg 2')
    tr.add_trigger(t0, 't0 all sid')
    tr.add_trigger(t1, dir)
    tr.add_trigger(t2, print)
    tr.add_trigger(t3, 't3 all reports')
    # print(tr)
    for h , arg in tr.get_handlers(Trigger('report.12331313133.status.off')):
        print_hand(*arg)
    print(tr.get_handlers(Trigger('report.3244242.status.off')))