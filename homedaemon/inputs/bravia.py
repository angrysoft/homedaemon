from homedaemon.inputs import BaseInput
from pytvremote import Bravia
import asyncio


class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'bravia'
        self.config = config
        self.tv = Bravia(config['tv']['ip'], macaddres=config['tv']['mac'])
        self.loop.create_task(self.get_tv_status())

    async def get_tv_status(self):
        while True:
            await asyncio.sleep(30)
            tvstatus = dict()
            if self.tv.power:
                tvstatus['status'] = 'on'
                tvstatus.update(self.tv.content_info())
            else:
                tvstatus['status'] = 'off'
                
            self.bus.emit_cmd({'cmd': 'report', 'sid': 'tv01',  'data': tvstatus})
            