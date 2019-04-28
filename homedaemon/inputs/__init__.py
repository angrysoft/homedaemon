import asyncio
import threading


class BaseInput:
    def __init__(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()

    def listen(self):
        print(f'listen {self.name} from {threading.current_thread()} thread')
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.loop.stop()
