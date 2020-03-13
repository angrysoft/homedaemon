from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'Test'
        self.automatic = False
        self.reversible = True
    
    def on(self):
        color = self.get_device('0x000000000545b741')
        color.on()
        color.bright(1)
        color.set_rgb({'red':0 ,'green':0, 'blue': 255})
    
    def off(self):
        color = self.get_device('0x000000000545b741')
        color.bright(70)
        color.set_ct_abx(3100)