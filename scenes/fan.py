from homedaemon.scenes import BaseScene
from datetime import datetime

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'bathrom fan'
        self.triggers = '158d0002abac97.channel_1.on'
        self.triggers = '158d0002abac97.channel_1.off'
    
    def on(self):
        wallsw = self.get_device('158d0002abac97')
        if wallsw.channel_1.is_on():
            self.sleep(300)
            if self.running and wallsw.channel_1.is_on():
                wallsw.channel_0.on()
        elif wallsw.channel_1.is_off():
            self.sleep(15)
            wallsw.channel_0.off()