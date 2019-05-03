from yeelight import YeelightWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__()
        self.name = 'Yeelight'
        self.yw = YeelightWatcher(queue, loop=self.loop)

    def quit(self):
        self.yw.stopping = True

