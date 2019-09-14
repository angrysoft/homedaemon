import json
from threading import Thread
from datetime import datetime, time
from time import sleep


class Scene:
    def __init__(self, path, queue_put):
        self.name = 'empty'
        self.cmds = {'on': [], 'off': []}
        self._load_scene_config(path)
        self.status = None
        self.queue_put = queue_put

    def _load_scene_config(self, path):
        try:
            with open(path, 'r') as jfscene:
                data = json.load(jfscene)
            self.name = data.get('name')
            self.cmds['on'] = data.get('on')
            self.cmds['off'] = data.get('off')
        except json.JSONDecodeError:
            pass

    def do(self, data):
        if 'data' in data:
            Commands(self.cmds.get(data['data'].get('status'), []),
                     self.queue_put).start()


class Commands(Thread):
    def __init__(self, cmds, queue_put=print):
        super().__init__()
        self.cmds = cmds
        self.queue_put = queue_put

    def run(self):
        self._run_cmds(self.cmds)

    def _run_cmds(self, cmds):
        for c in cmds:
            print(f'cmd : {c}')
            self.cmd(c.get('cmd'), c.get('args'))

    def cmd(self, cmd, args=None):
        if cmd == 'device':
            self.queue_put(args)
        if cmd == 'sleep':
            sleep(int(args))
        if cmd == 'check':
            self.chekc(args)

    def chekc(self, args):
        if len(args.get('if', 0)) < 3:
            raise ValueError('if list  3 elemnts')
        values  = args.get('if')
        status = {'time': TimeCheck,
                  'device': DevCheck}.get(values[0])(values[1:]).status
        print(args.get('if'), status)
        if status:
            self._run_cmds(args.get('then', []))
        else:
            self._run_cmds(args.get('else', []))


class TimeCheck:
    def __init__(self, args):
        op = args[0]
        self._now = datetime.now().time()
        self._value1 = time(*[int(i) for i in args[1].split(':')])
        if len(args) > 2:
            self._value2 = time(*[int(i) for i in args[2].split(':')])
        self.status = {'==': self.eq,
                       '>': self.gt,
                       '<': self.lt,
                       '<>':self.between}.get(op)()

    def eq(self):
        return self._now == self._value1

    def gt(self):
        return self._now > self._value1

    def lt(self):
        return self._now < self._value1
    
    def between(self):
        print(self._value1, self._now, self._value2)
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

class DevCheck:
    def __init__(self, op, value):
        self.status = False
        # TODO: ee and what ?


