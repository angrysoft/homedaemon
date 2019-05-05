from homedaemon.inputs import BaseInput
from serial import Serial, SerialException
from serial.tools.list_ports import comports
import json
import asyncio


class Input(BaseInput):
    def __init__(self, queue, baudrate=115200, port=None, timeout=0):
        super(Input, self).__init__(queue)
        self.name = 'Arduino'
        self.arduino = Serial()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.queue = queue
        self.stopping = False

    async def _connect(self):
        while not self.arduino.is_open:
            if self.stopping:
                break
            self.arduino.port = self.port
            self.arduino.baudrate = self.baudrate
            self.arduino.timeout = self.timeout
            if self.port is None:
                self.port = self._detect_port()
            if self.arduino.port:
                self.arduino.open()
                print(f'arduino connected')
                self.serial_reader()
                self.loop.add_reader(self.arduino, self.serial_reader)
            else:
                print(f'arduion is missing')
                await asyncio.sleep(3)

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
            self.queue.put(json.loads(data))
        except json.JSONDecodeError as er:
            print(f'{er}, : {data}')
        except SerialException:
            pass

    def run(self):
        self.loop.create_task(self._connect())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
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
