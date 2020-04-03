from homedaemon.scenes import BaseAutomation
from homedaemon.scenes import TimeCheck
from datetime import datetime

class Scene(BaseAutomation):
    def __init__(self,sid, daemon):
        super().__init__(sid, daemon)
        self.name = 'Lamap color temp'
        self.add_trigger('report.clock.time.sunset', self.on_time)
        self.place = 'Living room'
        self.lamp = self.get_device('0x0000000007e7bae0')
        self.clock = self.get_device('clock')
    
    def on_time(self):
        _sunset = datetime.now()
        while True:
            if lamp.is_on():
                lamp.ct_pc(50)
            self.sleep()
        
            