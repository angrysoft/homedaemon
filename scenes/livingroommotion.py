from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck
from datetime import datetime

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'Livingroom motion'
        self.triggers = '158d0002ec2fa6.status.motion'
        self.place = 'Living room'
    
    def on(self):
        sunrise = self.daemon.config['datetime']['sunrise']
        sunset = self.daemon.config['datetime']['sunset']
        if TimeCheck('<>', sunset, sunrise).status:
            lamp = self.get_device('0x0000000007e7bae0')
            lamp.on()
        else:
            lamp = self.get_device('0x0000000007e7bae0')
            lamp.off()
            