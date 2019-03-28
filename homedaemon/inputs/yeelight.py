from yeelight import YeelightWatcher
from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__(queue)
        self.name = 'Yeelight'
        yw = YeelightWatcher(queue)
