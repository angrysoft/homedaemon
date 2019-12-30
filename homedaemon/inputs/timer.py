from homedaemon.inputs import BaseInput
import asyncio
from datetime import datetime


class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'timer'
        self.config = config
        self.loop.create_task(self.timer())

    async def timer(self):
        while True:
            date = datetime.now()
            self.bus.emit_cmd({'cmd': 'report', 'sid': 'timer',  'data': {'time': f'{date.hour:02}:{date.minute:02}'}})
            if f'{date.hour:02}:{date.minute:02}' == self.config['datetime']['sunrise']:
                self.bus.emit_cmd({'cmd': 'report', 'sid': 'timer',  'data': {'time': 'sunrise'}})
            elif f'{date.hour:02}:{date.minute:02}' == self.config['datetime']['sunset']:
                self.bus.emit_cmd({'cmd': 'report', 'sid': 'timer',  'data': {'time': 'sunset'}})
            await asyncio.sleep(60)
