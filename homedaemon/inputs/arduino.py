from homedaemon.inputs import BaseInput
import serial
import os


class Input(BaseInput):
    def __init__(self, queue, baudrate=9600, port='/dev/ttyACM0', timeout=0):
        super(Input, self).__init__(queue)
        self.name = 'Arduino'
        self.arduino = serial.Serial()
        self.arduino.port = port
        self.arduino.baudrate = baudrate
        self.arduino.timeout = timeout

        if os.path.exists(self.arduino.port):
            self.arduino.open()
            print(f'arduino connected')
            self.loop.add_reader(self.arduino, queue)
