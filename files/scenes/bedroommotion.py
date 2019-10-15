from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'bedroom_motion'
        self.trigger = 'timer.time.14:25'
    
    def on(self):
        wallsw = self.get_device('158d0002a18c2b')
        wallsw.channel_1.on()
        self.sleep(5)
        wallsw.channel_1.off()