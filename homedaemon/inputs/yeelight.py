from yeelight import YeelightWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__()
        self.name = 'Yeelight'
        yw = YeelightWatcher(queue, loop=self.loop)
