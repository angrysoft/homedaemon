from homedaemon.io import BaseInput
from serial import Serial, SerialException
from serial.tools.list_ports import comports
import json
from sys import stderr
from os.path import exists
from time import sleep


class Input(BaseInput):
    def __init__(self, bus, config, loop):
        super(Input, self).__init__(bus, loop)
        self.name = 'Arduino'
        self.arduino = Serial()
        self.port = config['arduino']['port']
        if self.port is None or self.port == 'auto':
            self.port = self._detect_port()
        self.baudrate = config['arduino']['baudrate']
        self.timeout = 0
        self.stopping = False

    def _connect(self):
        while not self.arduino.is_open:
            if self.stopping:
                break
            self.arduino.port = self.port
            self.arduino.baudrate = self.baudrate
            self.arduino.timeout = self.timeout
            if self.port is None:
                return
            if self.arduino.port and exists(self.port):
                self.arduino.open()
                print(f'arduino connected: {self.port}')
                self.serial_reader()
                self.loop.add_reader(self.arduino, self.serial_reader)
            else:
                sleep(3)

    @staticmethod
    def _detect_port():
        port = None
        for p in comports():
            manufacturer = p.manufacturer
            if type(manufacturer) is str and 'arduino' in manufacturer.lower():
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
            self.bus.emit_cmd(json.loads(data))
        except json.JSONDecodeError as er:
            stderr.write(f'{er}, : {data}\n')
        except SerialException:
            pass

    def serial_write(self, value):
        try:
            msg = f'{value}\n'
            self.arduino.write(msg.encode())
        except json.JSONDecodeError as er:
            stderr.write(f'{er}, : {value}\n')
        except SerialException as err:
            self.daemon.logger.error(err)

    def run(self):
        self.loop.run_in_executor(None, self._connect)
        

