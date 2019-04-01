from angrysql import BaseModel, Column, Integer, String


class Models(BaseModel):
    mode_id = Column(Integer(), primary_key=True)
    name = Column(String(255), nullable=False)


class Devices(BaseModel):
    device_id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    model = Column(Integer(), foreignkey='models.model_id')
    sid = Column(String(255), unique=True)
    short_id = Column(String(255), unique=True)
    sort = Column(Integer(), default='0')
    voltage = Column(Integer())
    low_voltage = Column(Integer(), default='2800')


class DeviceData(BaseModel):
    data_id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    value = Column(String())
    device_id = Column(Integer(), nullable=False, foreignkey='devices.device_id')
