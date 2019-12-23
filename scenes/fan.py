from homedaemon.scenes import BaseScene
from datetime import datetime

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'hall motion'
        self.triggers = '158d0002abac97.channel_1.on'
    
    def on(self):
        wallsw = self.get_device('158d0002abac97')
        wallsw.channel_0.on()