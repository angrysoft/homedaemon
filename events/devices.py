from homedaemon.event import EventBase
from angrysql.sqlitedb import Connection
from angrysql import BaseModel, Column, Integer, String


class DeviceType(BaseModel):
    id = Column(Integer(), primary_key=True)
    type = Column(String(255), nullable=False)


class Devices(BaseModel):
    id = Column(Integer(), primary_key=True)
    device_type_id = Column(Integer(), nullable=False, foreignkey='device_type.id')


class DeviceTraits(BaseModel):
    id = Column(Integer(), primary_key=True)
    type = Column(String(255), nullable=False)


class Traits(BaseModel):
    traits_id = Column(Integer(), primary_key=True)
    device_traits_id = Column(Integer(), nullable=False, foreignkey='device_traits.id')
    device_id = Column(Integer(), foreignkey='devices.id')


class DeviceInfo:
    id = Column(Integer(), primary_key=True)
    manufacturer = Column(String(255))
    model = Column(String(255))
    hwVersion = Column(String(255))
    swVersion = Column(String(255))
    device_id = Column(Integer(), foreignkey='devices.id')


class CustomData(BaseModel):
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    value = Column(String())
    device_id = Column(Integer(), foreignkey='devices.id')


class Attributes(BaseModel):
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    value = Column(String())
    device_id = Column(Integer(), foreignkey='devices.id')


class _Devices:
    def __init__(self):
        self.id = -1
        self.type = ''
        self.traits = list()
        self.name = {
            'defaultNames': [],
            'name': '',
            'nicknames': []
        }
        self.willReportState = False
        self.roomHint = ''
        self.deviceInfo = {
            'manufacturer': '',
            'model': '',
            'hwVersion': '',
            'swVersion': ''
        }
        self.customData = {}
        self.attributes = {}


class Event(EventBase):
    pass
