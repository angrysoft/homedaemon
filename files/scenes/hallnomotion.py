from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'hall no motion'
        self.triggers = '158d00029a49ba.no_motion.120'
    
    def on(self):
        wallsw = self.get_device('158d0002a18c2b')
        wallsw.channel_0.off()
        wallsw.channel_1.off()
