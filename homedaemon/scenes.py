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
        condition, op, value = args.get('if')
        status = {'time': TimeCheck}.get(condition)(op, value).status
        print(args.get('if'), status)
        if status:
            self._run_cmds(args.get('then', []))
        else:
            self._run_cmds(args.get('else', []))


class TimeCheck:
    def __init__(self, op, value):
        self._now = datetime.now().time()
        self._value = time(*[int(i) for i in value.split(':')])
        self.status = {'==': self.eq,
                       '>': self.gt,
                       '<': self.lt}.get(op)()

    def eq(self):
        return self._now == self._value

    def gt(self):
        return self._now > self._value

    def lt(self):
        return self._now < self._value




