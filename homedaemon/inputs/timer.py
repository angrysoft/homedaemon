from homedaemon.inputs import BaseInput
import asyncio
from datetime import datetime


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'timer'
        self.loop.create_task(self.timer())

    async def timer(self):
        while True:
            date = datetime.now()
            self.queue.put({'cmd': 'report', 'sid': 'timer',  'data': {'time': f'{date.hour}:{date.minute:02}'}})
            await asyncio.sleep(60)