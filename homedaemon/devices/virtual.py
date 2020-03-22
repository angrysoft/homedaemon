from .base import BaseDevice, Dummy

class VirtualDevice:
    def __new__(cls, data, daemon):
        return {'timer': TimerDev}.get(data.get('model'), Dummy)(data, daemon)


class TimerDev(BaseDevice):
    def device_status(self):
        return {}