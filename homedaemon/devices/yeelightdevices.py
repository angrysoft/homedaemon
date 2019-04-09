from . import BaseDevice


class YeeligthDevice(BaseDevice):
    def __init__(self, data):
        super(YeeligthDevice, self).__init__(data)
        self.support = data.get('support')

    def do(self, **kwargs):
        pass