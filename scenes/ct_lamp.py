from homedaemon.scenes import BaseAutomation
from datetime import datetime

class Scene(BaseAutomation):
    def __init__(self,sid, daemon):
        super().__init__(sid, daemon)
        self.name = 'Lamp color temp'
        self.add_trigger('report.clock.time.sunset', self.on_time)
        self.place = 'Living room'
        self.lamp = self.get_device('0x0000000007e7bae0')
        self.clock = self.get_device('clock')
    
    def on_time(self):
        _sunset = datetime.now()
        _target_time = datetime(_sunset.year, _sunset.month, _sunset.day, 23, 0, 0)
        _delta - _target_time - _sunset
        _delta = _delta.seconds
        while _delta >= 0:
            if lamp.is_on():
                lamp.ct_pc(50)
            _delta -= 600
            print(_delta)
            self.sleep(600)
        self.lamp.ct_pc(0)
        
            