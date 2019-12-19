from threading import RLock, Thread

class BaseDevice:
    def __init__(self, data, daemon):
        self.daemon = daemon
        self.model = data.get('model')
        self.name = data.get('name')
        self.sid = data.get('sid')
        self.device_data = daemon.device_data[self.sid]
        self.lock = RLock()
        self.daemon.bus.on('report', self.sid, self.report, self.update_dev_data)
        self.daemon.bus.on('write', self.sid, self.write)
        self.daemon.bus.on('heartbeat', self.sid, self.heartbeat)

    def write(self, data):
        pass

    def heartbeat(self, data):
        pass
        
    def report(self, data):
        pass

    def update_dev_data(self, data):
        with self.lock:
            self.daemon.device_data[self.sid] = data['data']
    
    def get_value(self, value):
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

    def toggle(self):
        self.write({'data': {self.name: 'toggle'}})