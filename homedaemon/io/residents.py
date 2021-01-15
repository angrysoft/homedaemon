from homedaemon.io import BaseInput
from bluetooth import lookup_name
from pycouchdb import Server
import asyncio

class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'residents'
        srv = Server()
        self.residentsdb = srv.db('residents')
        self.loop.create_task(self.watch_residents())
    
    async def watch_residents(self):
        while True:
            for res in self.residentsdb:
                await self.check(res)
            await asyncio.sleep(25)
    
    async def check(self, resident):
        status = lookup_name(resident['phone_bt'], timeout=5)
        if status:
            if resident['in_home'] == False:
                self.residentsdb[resident['_id']]['in_home'] = True
                self.bus.emit_cmd({'cmd': 'residents', 'sid': resident['_id'],  'data': {'in_home': True}})
        else:
            if resident['in_home'] == True:
                self.residentsdb[resident['_id']]['in_home'] = False
                self.bus.emit_cmd({'cmd': 'residents', 'sid': resident['_id'],  'data': {'in_home': False}})
