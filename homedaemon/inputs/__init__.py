import asyncio


class BaseInput:
    def __init__(self, queue):
        self.loop = asyncio.get_event_loop()

    def listen(self):
        print(f'listen {self.name}')
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
