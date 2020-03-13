from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'Junior Lamp'
        self.triggers = '158d00033ef2d8.status.click'
    
    def on(self):
        lamp = self.get_device('235444403')
        if lamp:
            lamp.toggle()
            if lamp.is_on:
                lamp.set_bricct(1,1)