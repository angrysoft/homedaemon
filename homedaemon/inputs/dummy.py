from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__()
        self.name = 'dummy'
