from yeelight import YeelightWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__(queue)
        self.name = 'Yeelight'
        self.yw = YeelightWatcher(self.queue.put, loop=self.loop)



