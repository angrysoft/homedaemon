import asyncio


class BaseInput:
    def __init__(self, bus, loop):
        self.bus = bus
        self.loop = loop
 
    def stop(self):
        self.loop.stop()
        self.loop.close()
    
    def run(self):
        pass