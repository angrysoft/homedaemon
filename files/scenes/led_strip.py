from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'led_strip'
        self.triggers = '158d000200a020.status.click'
    
    def on(self):
        switch = self.get_device('158d00027d0065')
        if switch:
            switch.power.toggle()