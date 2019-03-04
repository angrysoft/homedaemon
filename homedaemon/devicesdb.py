from angrysql import BaseModel, Column, Integer, String


class Devices(BaseModel):
    device_id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    model = Column(String(255))
    sid = Column(String(255))
    short_id = Column(String(255))


class DeviceData(BaseModel):
    data_id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    value = Column(String())
    device_id = Column(Integer(), nullable=False, foreignkey='devices.device_id')
