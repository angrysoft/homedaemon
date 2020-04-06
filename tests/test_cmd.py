#!/usr/bin/python3
import json
import sys
from time import sleep
from datetime import datetime, time
from threading import Thread


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

class Time(time):
    # def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, time_str=None):
    #     if time_str:
    #         return cls.__new__(*[int(i) for i in time_str.split(':')])
    #     else:
    #        return cls.__new__(hour, minute, second, microsecond)
    
    def __add__(self, in_time):
        return self.to_sec() + in_time.to_sec()
    
    def __sub__(self, in_time):
        if self < in_time:
            raise ValueError
        return self.to_sec() - in_time.to_sec()
    
    def to_sec(self):
        return self.microsecond/1000000 + self.second + self.minute * 60 + self.hour * 3600

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     sys.exit()
    # with open(sys.argv[1]) as jfile:
    #     cmds = json.load(jfile)
    #     cmd = Commands(cmds.get('on'))
    #     cmd.run()
    t = Time(22)
    t1 = Time(23)
    print(t > t1)
    print(t.to_sec(), t1.to_sec())
    print(t1 - t)
    print(t1+t)