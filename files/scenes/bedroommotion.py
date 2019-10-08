from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'bedroom_motion'
    
    def on(self):
        if TimeCheck('<>', "22:00", '7:00').status:
            bslamp = self.get_device('0x000000000545b741')
            bslamp.power.on()
            self.sleep(25)
            bslamp.power.off()
