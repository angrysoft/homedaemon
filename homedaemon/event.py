from homedaemon.devicesdb import *
from angrysql.sqlitedb import Connection


class EventBase:
    def __init__(self):
        self._event = 'event'
        self.ctrl = None
        self.args = None
        self._type = ''
        config = {'dbfile': 'device.db'}
        self.db = Connection(config)
        self.db.create_tables(Devices, DeviceData)

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._event

    def do(self, data):
        pass
