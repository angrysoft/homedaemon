from homedaemon.inputs import BaseInput
import asyncio
from datetime import datetime


class Input(BaseInput):
    def __init__(self, queue, config):
        super(Input, self).__init__(queue)
        self.name = 'timer'
        self.config = config
        self.loop.create_task(self.timer())

    async def timer(self):
        while True:
            date = datetime.now()
            self.queue.put({'cmd': 'report', 'sid': 'timer',  'data': {'time': f'{date.hour:02}:{date.minute:02}'}})
            if f'{date.hour:02}:{date.minute:02}' == self.config['datetime']['sunrise']:
                self.queue.put({'cmd': 'report', 'sid': 'timer',  'data': {'time': 'sunrise'}})
            elif f'{date.hour:02}:{date.minute:02}' == self.config['datetime']['sunset']:
                self.queue.put({'cmd': 'report', 'sid': 'timer',  'data': {'time': 'sunset'}})
            await asyncio.sleep(60)
