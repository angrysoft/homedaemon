from .base import BaseDevice, Dummy
import asyncio
from datetime import datetime


class VirtualDevice:
    def __new__(cls, data, daemon):
        return {'clock': ClockDev}.get(data.get('model'), Dummy)(data, daemon)


class ClockDev:
    def __init__(self, data, daemon):
        self.daemon = daemon
        self.model = data.get('model')
        self.name = data.get('name')
        self.sid = data.get('sid')
        self.daemon.loop.create_task(self.timer())
        self._time = dict()

    async def timer(self):
        await self._to_change_min()
        while True:
            date = datetime.now()
            self._time = {'hour': date.hour, 'minute': date.minute, 'sec': date.second}
            self.daemon.bus.emit(f'report.clock.time.{self.time}')
            if self.time == self.daemon.config['datetime']['sunrise']:
                self.daemon.bus.emit(f'report.clock.time.sunrise')
            elif self.time == self.daemon.config['datetime']['sunset']:
                self.daemon.bus.emit(f'report.clock.time.sunset')
            await asyncio.sleep(60)
            
    async def _to_change_min(self):
        while datetime.now().second:
            await asyncio.sleep(1)
    
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