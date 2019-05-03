from homedaemon.inputs import BaseInput


class Input(BaseInput):
    def __init__(self, queue):
        super(Input, self).__init__()
        self.name = 'dummy'

    def stop(self):
        # pass
        self.loop.stop()
        print('stop loop')
        # self.gw.transport.close()
        # print('transport close')
        # self.loop.close()
        # print(f'{self.name} stops')
