#!/usr/bin/python3

from aquara import Gateway
from couchdb import Server
from yeelight import Yeelight
from urllib.parse import urlparse



class Register:
    def __init__(self):
        self.db = Server()
        self.devices = None
        self.devices_data = None

    def clear_db(self):
        print('Remove all device and device data')
        if 'devices' in self.db:
            self.db.delete('devices')
        if 'devices-data' in self.db:
            self.db.delete('devices-data')

    def create_db(self):
        print('Creating db')
        self.devices = self.db.create('devices')
        self.devices_data = self.db.create('devices-data')

    @staticmethod
    def dev_list():
        gw = Gateway()
        ye = Yeelight()
        list_devs = gw.read_all_devices()
        list_devs.append({'cmd': 'report', 'model': 'dallastemp',
                          'sid': 'dallasT1', 'data': {'temp': 0}})
        list_devs.append({'cmd': 'report', 'model': 'rgbstrip', 'sid': 'rgb01',
                          'data': {'red': 0, 'green': 0, 'blue': 0}})
        list_devs.append({'cmd': 'write', 'model': 'bravia', 'sid': 'tv01', 'ip': '192.168.1.129',
                          'mac': 'FC:F1:52:2A:9B:1E',
                          'data': {'button': ''}})
        ye.discover()
        for bulb in ye.devices:
            d = ye.devices[bulb]
            url = urlparse(d.get('location'))
            del d['location']
            d['sid'] = d.pop('id')
            d['ip'] = url.hostname
            d['port'] = url.port
            d['data'] = {'power': d.pop('power'),
                         'bright': d.pop('bright'),
                         'color_mode': d.pop('color_mode'),
                         'ct': d.pop('ct'),
                         'rgb': d.pop('rgb'),
                         'hue': d.pop('hue'),
                         'sat': d.pop('sat')
                         }
            d['support'].append('on')
            d['support'].append('off')
            list_devs.append(d)

        return list_devs

    def registering(self):
        list_devs = self.dev_list()

        print('Registering device:')
        for d in list_devs:
            if 'cmd' in d:
                del d['cmd']
            data = d.get('data')
            del d['data']

            data['sid'] = d.get('sid')
            if 'name' not in d:
                d['name'] = ''
            print('\t', d.get('model'), d.get('sid'))

            self.devices[d.get('sid')] = d
            self.devices_data[d.get('sid')] = data

    # def add_index(self):
    #     print(f"Creating index on device: {db.devices.create_index([('sid', TEXT)], unique=True)}")
    #     print(f"Creating index on device data: {db.devices_data.create_index([('sid', TEXT)], unique=True)}")


if __name__ == '__main__':
    r = Register()
    r.clear_db()
    r.create_db()
    r.registering()
