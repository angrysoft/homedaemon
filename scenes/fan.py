from homedaemon.scenes import BaseScene
from datetime import datetime
from threading import Timer

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'bathrom fan'
        self.triggers = '158d0002abac97.channel_1.on'
        self.triggers = '158d0002abac97.channel_1.off'
        self.timer_fan_on = None
        
    def on(self):
        wallsw = self.get_device('158d0002abac97')
        if wallsw.channel_1.is_on():
            self.timer_fan_on(10, self.fan_on, wallsw)
                
        elif wallsw.channel_1.is_off():
            if self.timer_fan_on:
                self.timer_fan_on.cancel()
            self.sleep(5)
            if wallsw.channel_1.is_off():
                wallsw.channel_0.off()
    
    def fan_on(self, wallsw):
        if self.running and wallsw.channel_1.is_on():
                wallsw.channel_0.on()
                self.timer_fan_on = None
                