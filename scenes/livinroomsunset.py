from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck
from datetime import datetime

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'Livingroom sunset'
        self.triggers = 'timer.time.sunset'
    
    def on(self):
        tv = self.get_device('tv01')
        if tv.power:
            lamp = self.get_device('0x0000000007e7bae0')
            lamp.on()
            