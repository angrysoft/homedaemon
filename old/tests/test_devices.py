import unittest
from homedaemon.devices import Devices


class TestDevices(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.devices = Devices()
    
    
    def test_get_devices_list(self):
        ret = self.devices.get_devices_list()
        