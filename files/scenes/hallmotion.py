from homedaemon.scenes import BaseScene
from homedaemon.scenes import TimeCheck

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'hall_motion'
        self.trigger = '158d00029a49ba.status.motion'
    
    # def on(self):
    #     if TimeCheck('<>', "18:00", '7:00').status:
    #         wallsw = self.get_device('158d0002a18c2b')
    #         wallsw.channel_1.on()
    #         self.sleep(25)
    #         wallsw.channel_1.off()
    
    def on(self):
        entrance = self.get_device('158d0002b74c28')
        wallsw = self.get_device('158d0002a18c2b')
        print(entrance.get_value('status'))
        if entrance.get_value('status') == 'open':
            wallsw.all_on()
            self.sleep(5)
            wallsw.all_off()
        else:
            wallsw.channel_1.on()
            self.sleep(5)
            wallsw.channel_1.off()