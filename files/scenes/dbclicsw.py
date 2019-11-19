from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'dbclick'
        self.triggers = '158d000200a020.status.double_click'
    
    def on(self):
        kitchen_lamp = self.get_device('158d0002bffe5a')
        if kitchen_lamp:
            kitchen_lamp.channel_0.toggle()