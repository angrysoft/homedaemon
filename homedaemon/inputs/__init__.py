import asyncio
from threading import current_thread


class BaseInput:
    def __init__(self):
        self.iniTh = str(current_thread())
        print(f'init from {str(current_thread())}')
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def listen(self):
        print(f'listen {self.name} from {current_thread()} thread init {self.iniTh}')
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def stop(self):
        self.loop.stop()
        self.loop.close()
