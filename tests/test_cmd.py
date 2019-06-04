#!/usr/bin/python3
import json
import sys
from time import sleep


class TimeCheck:
    def __init__(self, op, arg):
        self.status = {'==': self.eq,
                      '>': self.gt}.get(op)(arg)

    def eq(self, arg):
        pass

    def gt(self, arg):
        pass


class Commands:
    def __init__(self, cmds, queue_put=print):
        self.cmds = cmds
        self.queue_put = queue_put

    def run(self):
        for c in self.cmds:
            print(c)
            cmd = c.get('cmd')
            args = c.get('args')
            if cmd == 'device':
                self.queue_put(args)
            if cmd == 'sleep':
                print(f'sleep {args}')
            if cmd == 'check':
                if {'if', 'op', 'then'}.issubset(c):
                    self.chekc(c)

    def chekc(self, args):
        condtion, arg = args['if'].popitem()
        print(condtion, arg)
        return {'time': TimeCheck}.get(condtion)(args['op'], arg)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    with open(sys.argv[1]) as jfile:
        cmds = json.load(jfile)
        c = Commands(cmds.get('on'))
        c.run()