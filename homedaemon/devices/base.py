from threading import RLock, Thread

class BaseDevice:
    def __init__(self, data, daemon):
        self.daemon = daemon
        self.model = data.get('model')
        self.name = data.get('name')
        self.sid = data.get('sid')
        self.lock = RLock()
        self.daemon.bus.add_trigger(f'report.{self.sid}.*.*', self.report)
        self.daemon.bus.add_trigger(f'write.{self.sid}.*.*', self.write)
        self.daemon.bus.add_trigger(f'heartbeat.{self.sid}.*.*', self.heartbeat)

    def write(self, data):
        pass

    def heartbeat(self, data):
        pass
        
    def report(self, data):
        pass

    def update_dev_data(self, data):
        import warnings
        warnings.warn(f"deprecated {self.sid} update_dev_data", DeprecationWarning)
        
        with self.lock:
            self.daemon.device_data[self.sid] = data['data']
    
    def get_value(self, value):
        import warnings
        warnings.warn(f"deprecated {self.sid} get_value", DeprecationWarning)
        if value in self.daemon.device_data[self.sid]:    
            return self.daemon.device_data[self.sid][value]
        else:
            return None
        

class ButtonOnOff:
    def __init__(self, name, write):
        self.name = name
        self.write = write

    def on(self):
        self.write({'data': {self.name: 'on'}})

    def off(self):
        self.write({'data': {self.name: 'off'}})
    
    def toggle(self):
        self.write({'data': {self.name: 'toggle'}})


class ButtonToggleOnOff(ButtonOnOff):
    pass
        

class Dummy:
    def __init__(self, *args, **kwargs):
        pass
    
    def device_status(self):
        return {}