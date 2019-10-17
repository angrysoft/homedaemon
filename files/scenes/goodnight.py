from homedaemon.scenes import BaseScene

class Scene(BaseScene):
    def __init__(self, daemon):
        super().__init__(daemon)
        self.name = 'goodnight'
        self.automatic = False
    
    def on(self):
        dev_to_off = ['']
        bslamp = self.get_device('0x000000000545b741')
        bslamp.on()
        