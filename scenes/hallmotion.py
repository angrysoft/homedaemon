from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck
from datetime import datetime

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'hall motion'
        self.triggers = '158d00029a49ba.status.motion'
    
    def on(self):
        sunrise = self.daemon.config['datetime']['sunrise']
        sunset = self.daemon.config['datetime']['sunset']
        if TimeCheck('<>', sunset, sunrise).status:
            entrance = self.get_device('158d0002b74c28')
            wallsw = self.get_device('158d0002a18c2b')
            if entrance.get_value('status') == 'open':
                wallsw.all_on()
                lamp = self.get_device('0x0000000007e7bae0')
                lamp.on()
                self.sleep(25)
                wallsw.channel_1.off()
                self.sleep(10)
                wallsw.channel_2.off()
            else:
                wallsw.channel_1.on()
                self.sleep(25)
                wallsw.channel_1.off()
