#!/usr/bin/python3
import json
import sys
from time import sleep
from datetime import datetime, time


class TimeCheck:
    def __init__(self, op, value):
        self._now = datetime.now().time()
        self._value = time(*[int(i) for i in value.split(':')])
        self.status = {'==': self.eq,
                       '>': self.gt}.get(op)()

    def eq(self):
        return self._now == self._value

    def gt(self):
        return self._now > self._value

    def lt(self):
        return self._now < self._value


class Commands:
    def __init__(self, cmds, queue_put=print):
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
            print(f'sleep {args}')
        if cmd == 'check':
            self.chekc(args)

    def chekc(self, args):
        if len(args.get('if', 0)) < 3:
            raise ValueError('if list  3 elemnts')
        condition, op, value = args.get('if')
        status = {'time': TimeCheck}.get(condition)(op, value).status
        print(args.get('if'), status)
        if status:
            self._run_cmds(args.get('then', []))
        else:
            self._run_cmds(args.get('else', []))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    with open(sys.argv[1]) as jfile:
        cmds = json.load(jfile)
        cmd = Commands(cmds.get('on'))
        cmd.run()
