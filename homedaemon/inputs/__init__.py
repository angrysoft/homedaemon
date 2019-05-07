import asyncio
from threading import Thread


class BaseInput(Thread):
    def __init__(self, queue):
        super().__init__()
        self.setDaemon(True)
        self.queue = queue
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print('omg')

    def stop(self):
        self.loop.stop()
        self.loop.close()
