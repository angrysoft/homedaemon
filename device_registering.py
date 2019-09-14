#!/usr/bin/python3

from aquara import Gateway
from pycouchdb import Server
from yeelight import Yeelight
from urllib.parse import urlparse
import json


class Register:
    def __init__(self):
        self.srv = Server()
        self.devices = None
        self.devices_data = None
        self.config = None
        self.names = {'0x000000000545b741': 'Bedroom Lamp',
                      '0x0000000007e7bae0': 'Living room lamp',
                      '158d00027d0065': 'Kitchen Strip',
                      '158d000283b219': 'Bedroom speakers',
                      '158d00029b1929': 'Living room ',
                      '158d0002a16338': 'Bedroom',
                      '158d0002a18c2b': 'Hall',
                      '158d0002abac97': 'Bathroom',
                      '158d0002bffe5a': 'Kitchen',
                      '158d00024e2e5b': 'Outside',
                      '158d0002c9d230': 'Bathroom',
                      '158d0002e966b9': 'Living Room',
                      '158d00025d84a6': 'Outside',
                      '158d000208d668': 'Bedroom',
                      '158d0002ec2fa6': 'Living Room',
                      '158d00029a49ba': 'Hall',
                      '158d0002ec03fe': 'Bedroom',
                      '158d000200a020': 'Kitchen Switch',
                      '158d0002b74c28': 'Entrance',
                      '158d0002a13819': 'Living room Door',
                      '158d0002a67612': 'Bedroom window',
                      'tv01': 'Bravia',
                      'rgb01': 'Tv Rgb',
                      '7c49eb17b2a0': 'Gateway'}

    def clear_db(self):
        print('Remove all device and device data')
        if 'devices' in self.srv:
            self.srv.delete('devices')
        if 'devices-data' in self.srv:
            self.srv.delete('devices-data')
        if 'config' in self.srv:
            self.srv.delete('config')

    def create_db(self):
        print('Creating db')
        self.srv.create('devices')
        self.srv.create('devices-data')
        self.srv.create('config')
        
    def accessing_db(self):
        print('accessing db')
        self.devices = self.srv['devices']
        self.devices_data = self.srv.db('devices-data')
        self.config = self.srv.db('config')

    @staticmethod
    def dev_list():
        gw = Gateway()
        ye = Yeelight()
        gt = gw.whois()

        list_devs = gw.read_all_devices()
        list_devs.append(gw.read_device(gt.get('sid')))
        print('Find aquara devices')
        list_devs.append({'cmd': 'report', 'model': 'dallastemp',
                          'sid': 'dallasDS0', 'data': {'temp': 0}})
        list_devs.append({'cmd': 'report', 'model': 'rgbstrip', 'sid': 'rgb01',
                          'data': {'red': 0, 'green': 0, 'blue': 0,
                                   'default': {'red': 0, 'green': 0, 'blue': 0},
                                   'status': 'off'}})
        list_devs.append({'cmd': 'write', 'model': 'bravia', 'sid': 'tv01', 'ip': '192.168.1.129',
                          'mac': 'FC:F1:52:2A:9B:1E',
                          'data': {'button': ''}})
        print('Find custom devices')
        ye.discover()
        print('find yeelight devices')
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
            d['name'] = self.names.get(d.get('sid'), '....')
            if d['name'] == 'Hall' and d['model'] == 'sensor_motion.aq2':
                d['on_motion'] = 'hall_motion'
                d['on_nomotion'] = {'120':'hall_no_motion'}
            elif d['name'] == 'Kitchen Switch' and d['model'] == 'sensor_switch.aq2':
                d['on_click'] = 'led_strip'
            print(f"\t {d.get('model')}  {d.get('sid')} {d.get('name')}")

            self.devices[d.get('sid')] = d
            self.devices_data[d.get('sid')] = data

    def add_config(self):
        with open('files/angryhome.json') as jconf:
            config = json.load(jconf)

            for c in config:
                self.config[c] = config[c]
            self.config['user'] = {'user': 'admin',
                                   'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'}
            print('Config added')

    # def add_index(self):
    #     print(f"Creating index on device: {db.devices.create_index([('sid', TEXT)], unique=True)}")
    #     print(f"Creating index on device data: {db.devices_data.create_index([('sid', TEXT)], unique=True)}")


if __name__ == '__main__':
    r = Register()
    r.clear_db()
    r.create_db()
    r.accessing_db()
    r.registering()
    r.add_config()

