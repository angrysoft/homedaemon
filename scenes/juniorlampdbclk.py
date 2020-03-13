from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'Junior Lamp dbclik'
        self.triggers = '158d00033ef2d8.status.double_click'
    
    def on(self):
        lamp = self.get_device('235444403')
        if lamp:
            if lamp.bright < 100:
                lamp.set_bricct(100,100)
            elif lamp.bright > 1:
                lamp.set_bricct(1,1)