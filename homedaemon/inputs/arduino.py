from homedaemon.inputs import BaseInput
from serial import Serial, SerialException
from serial.tools.list_ports import comports
import json


class Input(BaseInput):
    def __init__(self, queue, baudrate=115200, port=None, timeout=0):
        super(Input, self).__init__()
        self.name = 'Arduino'
        self.arduino = Serial()
        if port is None:
            port = self._detect_port()
        self.arduino.port = port
        self.arduino.baudrate = baudrate
        self.arduino.timeout = timeout
        self.queue = queue

        if self.arduino.port:
            self.arduino.open()
            print(f'arduino connected')
            self.serial_reader()
            self.loop.add_reader(self.arduino, self.serial_reader)
        else:
            print(f'arduion is missing')

    def _detect_port(self):
        port = None
        for p in comports():
            if 'arduino' in p.description.lower():
                port = p.device
        return port

    def serial_reader(self):
        """"""
        try:
            b = self.arduino.read().decode()
            data = ''
            while not b == '\n':
                data += b
                b = self.arduino.read().decode()
            self.queue(json.loads(data))
        except json.JSONDecodeError as er:
            print(f'{er}, : {data}')
        except SerialException:
            pass

# class Output(asyncio.Protocol):
#     def __init__(self):
#         self.transport = None
#
#     def connection_made(self, transport):
#         self.transport = transport
#         print('port opened', transport)
#         transport.serial.rts = False
#         transport.write(b'hello world\n')
#
#     def data_received(self, data):
#         print('data received', repr(data))
#         self.transport.close()
#
#     def connection_lost(self, exc):
#         print('port closed')
#         asyncio.get_event_loop().stop()
#
#
# class Input(BaseInput):
#     def __init__(self, queue, baudrate=9600, port='/dev/ttyACM2', timeout=0):
#         super(Input, self).__init__(queue)
#         self.name = 'Arduino'
#         self.queue = queue
#         coro = serial.aio.create_serial_connection(self.loop, Output, port, baudrate=baudrate)
#         self.loop.run_until_complete(coro)
