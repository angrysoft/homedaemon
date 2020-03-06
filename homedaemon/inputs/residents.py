from homedaemon.inputs import BaseInput
from bluetooth import lookup_name
from pycouchdb import Server
import asyncio

class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'residents'
        srv = Server()
        residentsdb = srv.db('residents')
        self.residents = [r for r in residentsdb]
        self.loop.create_task(self.watch_residents())
    
    async def watch_residents(self):
        while True:
            for res in self.residents:
                status = lookup_name(res['phone_bt'], timeout=5)
                if status:
                    print(f"{res['name']} is in home")
                else:
                    print(f"{res['name']} is not in home")
            await asyncio.sleep(15)
        
        # self.yw = YeelightWatcher(self.bus.emit_cmd, loop=self.loop)