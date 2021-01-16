import asyncio
from typing import Any, Optional, List, Dict, Callable

class Trigger:
    def __init__(self, trigger: str):
        if type(trigger) is str:
            _values = trigger.split('.', 3)
            if len(_values) == 4:
                self.cmd,self.sid, self.event, self.value = _values
            else:
                raise ValueError(f'incorrect trigger format:  {trigger}')
        
    def __repr__(self):
        return f'Trigger: {self.cmd}.{self.sid}.{self.event}.{self.value}'
    
    
class TriggerDict:
    def __init__(self):
        self._data = dict()
    
    def setdefault(self, key, value):
        return self._data.setdefault(key, value)
    
    def getkeys(self, keyname:str) -> List[Any]:
        ret = list()
        if keyname in self._data:
            ret.append(self._data[keyname])
        if '*' in self._data:
            ret.append(self._data['*'])
        return ret
    
    def get_path_key(self, *keys:str):
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
    _instance: object = None
    
    def __new__(cls, loop:Optional[asyncio.AbstractEventLoop] = None) -> Any:
        if Bus._instance is None:
            if loop is not None:
                cls.loop = loop
            else:
                cls.loop = asyncio.get_event_loop()
            cls.running = []
            cls._triggers:TriggerDict = TriggerDict()
            Bus._instance = object.__new__(cls)
        return cls._instance
    
    def add_trigger(self, trigger:str, handler:Callable[[], None], *args:Any) -> None:
        _trigger = Trigger(trigger)
        cmd:TriggerDict = self._triggers.setdefault(_trigger.cmd, TriggerDict())
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
    
    def emit(self, event:str, *payload:Any) -> None:
        self.loop.run_in_executor(None, self._run_handler, event, *payload)
        
    def _run_handler(self, event:str, *payload:Any) -> None:
        trigger = Trigger(event)
        
        for handler, args in self.get_handlers(trigger):
            if self.is_async(handler):
                if payload:
                    task = asyncio.run_coroutine_threadsafe(handler(*payload), self.loop)
                else:
                    task = asyncio.run_coroutine_threadsafe(handler(), self.loop)
            else:
                handler_with_args: List[Any] = list()
                # handler_with_args.append(handler)
                handler_with_args.extend(args)
                handler_with_args.extend(payload)
                if handler_with_args:
                    handler(*handler_with_args)
                else:
                    handler()
                # try:
                # self.loop.run_in_executor(None, *handler_with_args)
                # except Exception:
                # log error
                
    def emit_cmd(self, event:Dict[str, Any]):
        try:
            _data = event['data'].copy()
            for key in _data:
                self.emit(f"{event['cmd']}.{event['sid']}.{key}.{_data[key]}",
                          {'cmd': event['cmd'],
                           'sid': event['sid'],
                           'data': {key: _data[key]}})
        except KeyError:
            pass
        
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