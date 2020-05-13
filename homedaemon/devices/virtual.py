from .base import BaseDevice, Dummy
from urllib import request
from datetime import datetime
import asyncio
import json


class Driver:
    def __new__(cls, data, daemon):
        return {'clock': ClockDev}.get(data.get('model'), Dummy)(data, daemon)


class ClockDev:
    def __init__(self, data, daemon):
        self.daemon = daemon
        self.model = data.get('model')
        self.name = data.get('name')
        self.sid = data.get('sid')
        self.daemon.loop.create_task(self.timer())
        self.daemon.bus.add_trigger('report.clock.time.01:00', self.sun_info)
        self._time = dict()
        self.sun_info()

    async def timer(self):
        await self._to_change_min()
        while True:
            date = datetime.now()
            self._time = {'hour': date.hour, 'minute': date.minute}
            self.daemon.bus.emit(f'report.clock.time.{self.time}')
            if self.time ==self.sunrise:
                self.daemon.bus.emit(f'report.clock.time.sunrise')
            elif self.time == self.sunset:
                self.daemon.bus.emit(f'report.clock.time.sunset')
            await asyncio.sleep(60)
            
    async def _to_change_min(self):
        while datetime.now().second:
            await asyncio.sleep(1)
    
    def sun_info(self):
        utcoffset = datetime.now() - datetime.utcnow()
        with request.urlopen('https://api.sunrise-sunset.org/json?lat=52.2319581&lng=21.0067249&formatted=0') as r:
            try:    
                ret = json.loads(r.read().decode())
                if 'results' in  ret:
                    ret = ret['results']
                    sunrise_utc = datetime.fromisoformat(ret.get('sunrise', '')) + utcoffset
                    sunset_utc = datetime.fromisoformat(ret.get('sunset', '')) + utcoffset
                    self._time['sunrise'] = f'{sunrise_utc.hour:02}:{sunrise_utc.minute:02}'
                    self._time['sunset'] = f'{sunset_utc.hour:02}:{sunset_utc.minute:02}'
            except json.JSONDecodeError:
                pass
    
    @property
    def sunrise(self) ->str:
        return self._time.get('sunrise')
    
    @property
    def sunset(self) ->str:
        return self._time.get('sunset')
        
    @property
    def hour(self) -> int:
        return self._time.get('hour')
    
    @property
    def minute(self) -> int:
        return self._time.get('minute')
    
    @property
    def time(self) -> str:
        return f'{self.hour:02}:{self.minute:02}'
    
    def device_status(self):
        date = datetime.now()
        return {'time': f'{date.hour:02}:{date.minute:02}'}