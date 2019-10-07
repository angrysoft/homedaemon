from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'hall_motion'
        self.scene_type = 'automatic'
    
    def on(self):
        if TimeCheck('<>', "18:00", '7:00').status:
            wallsw = self.get_device('158d0002a18c2b')
            wallsw.channel_1.on()
            self.sleep(25)
            wallsw.channel_1.off()
