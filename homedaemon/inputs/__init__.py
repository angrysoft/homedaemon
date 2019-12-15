import asyncio
from threading import Thread


class BaseInput(Thread):
    def __init__(self, bus, loop):
        super().__init__()
        self.setDaemon(True)
        self.bus = bus
        self.loop = loop
 
    def stop(self):
        self.loop.stop()
        self.loop.close()
