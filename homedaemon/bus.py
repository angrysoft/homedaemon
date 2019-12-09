
import asyncio


class Bus:
    def __init__(self):
        self._events = dict()
        
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
        print(f'debug: {event}')
        awitable = list()
        try:
            for ev in self._events[event.get('cmd')][event.get('sid')]:
                # awitable.append(ev(event))
                ev(event)
            # self._event(awitable)
            # Broadcast 
            for ev in self._events[event.get('cmd')]['*']:
                print(f'call {ev},')
                ev(event)
        except KeyError as err:
            print(f'emit {err}')
    
    def _event(self, awitable):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(awitable))
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
