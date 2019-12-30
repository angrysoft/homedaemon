from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'alarm'
        self.triggers = '158d00029a49ba.status.motion'
        self.triggers = '158d0002ec03fe.status.motion'
    
    def on(self):
        pass