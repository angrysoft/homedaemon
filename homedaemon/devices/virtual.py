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

    async def timer(self):
        while True:
            date = datetime.now()
            _time = f'{date.hour:02}:{date.minute:02}'
            self.daemon.bus.emit(f'report.clock.time.{_time}')
            if _time == self.daemon.config['datetime']['sunrise']:
                self.daemon.bus.emit(f'report.clock.time.sunrise')
            elif _time == self.daemon.config['datetime']['sunset']:
                self.daemon.bus.emit(f'report.clock.time.sunset')
            await asyncio.sleep(60)
    
    def device_status(self):
        date = datetime.now()
        return {'time': f'{date.hour:02}:{date.minute:02}'}