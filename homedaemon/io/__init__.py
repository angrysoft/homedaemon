from homedaemon.logger import Logger
import asyncio
import importlib


class BaseInput:
    def __init__(self, bus, loop):
        self.name = ""
        self.bus = bus
        self.loop = loop

    def stop(self):
        self.loop.stop()
        self.loop.close()

    def run(self):
        pass


class Inputs:
    def __init__(self, bus, loop):
        self._inputs = dict()
        self.bus = bus
        self.loop = loop
        self.logger = Logger()

    def register_inputs(self, input_list):
        for _input_name in input_list:
            _input = importlib.import_module(f"homedaemon.inputs.{_input_name}")
            inst = _input.Input(self.bus, self.config, self.loop)
            self._inputs[inst.name] = inst
            self.logger.info(f"load input: {inst.name}")
            self.inputs[inst.name].run()

    def get(self, key):
        if key in self._inputs:
            return self._inputs[key]
        else:
            return None

    def __contains__(self, key):
        if key in self._inputs:
            return True
        else:
            return False

    def __getitem__(self, key):
        return self.get(key)
