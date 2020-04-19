#!/usr/bin/python3

from pyxiaomi import Gateway
from pycouchdb import Server
from pyxiaomi import Yeelight
from pytvremote import Bravia
from pysonoff import Discover
from urllib.parse import urlparse
import importlib
importlib.sys.path.append('../')
importlib.sys.path.append('../scenes')
from homedaemon.scenes import BaseAutomation, BaseScene
import json
import os


class Register:
    def __init__(self):
        self.srv = Server()
        self.devices = None
        self.devices_data = None
        self.config = None
        self.residents = None
        self.names = {
            '158d0002a13819': {'name': 'Door', 'place': 'Living room'},
            '158d00029b1929': {'name': 'Light', 'place': 'Living room'},
            '158d0002e966b9': {'name': 'Sensor', 'place': 'Living room'},
            '158d0002ec2fa6': {'name': 'Motion', 'place': 'Living room'},
            '568A6295FB9FE3648F78F0146D20E557749B32B7': {'name': 'Tv', 'place': 'Living room'},
            'rgb01': {'name': 'Tv strip', 'place': 'Living room'},
            '7c49eb17b2a0': {'name': 'Gateway', 'place': 'Living room'},
            'dallasDS0': {'name': 'Arduino', 'place': 'Living room'},
            '0x0000000007e7bae0': {'name': 'Lamp', 'place': 'Living room'},
            '0x0000000007200259': {'name': 'Desk lamp', 'place': 'Living room'},
            '0x000000000545b741': {'name': 'Bed Lamp', 'place': 'Bedroom'},
            '158d0002a67612': {'name': 'Window', 'place': 'Bedroom'},
            '158d00033ef2d8': {'name': 'Lamp Switch', 'place': 'Bedroom'},
            '235444403': {'name': 'Johnie lamp', 'place': 'Bedroom'},
            '158d00027d0065': {'name': 'Strip', 'place': 'Kitchen'},
            '158d0002bffe5a': {'name': 'Light', 'place': 'Kitchen'},
            '158d000200a020': {'name': 'Switch', 'place': 'Kitchen'},
            '158d00044638db': {'name': 'Window', 'place': 'Kitchen'},
            '158d0002abac97': {'name': 'Light', 'place': 'Bathroom'},
            '1000b6063e': {'name': 'Mirror Lamp', 'place': 'Bathroom'},
            '158d0002c9d230': {'name': 'Sensor', 'place': 'Bathroom'},
            '158d00024e2e5b': {'name': 'Light', 'place': 'Outside'},
            '158d00025d84a6': {'name': 'Sensor', 'place': 'Outside'},
            '158d000283b219': {'name': 'Socket', 'place': 'Bedroom'},
            '158d000208d668': {'name': 'Sensor', 'place': 'Bedroom'},
            '158d0002ec03fe': {'name': 'Motion', 'place': 'Bedroom'},
            '158d0002a16338': {'name': 'Light', 'place': 'Bedroom'},
            '158d0002a18c2b': {'name': 'Light', 'place': 'Hall'},
            '158d00029a49ba': {'name': 'Motion', 'place': 'Hall'},
            '158d0002b74c28': {'name': 'Entrance', 'place': 'Hall'},
            'clock': {'name': 'clock', 'place': ''}
        }

    def clear_db(self):
        print('Remove all device and device data')
        if 'devices' in self.srv:
            self.srv.delete('devices')
            
    def create_db(self):
        print('Creating db')
        self.srv.create('devices')
        
        
    def accessing_db(self):
        print('accessing db')
        self.devices = self.srv['devices']
        

    def dev_list(self):
        gw = Gateway()
        ye = Yeelight()
        gt = gw.whois()
        sc = self.get_scenes()
        sof = Discover()
        list_devs = list()
        
        for dev in gw.read_all_devices():
            dev['family'] = 'aqara'
            list_devs.append(dev)
        gateway = gw.read_device(gt.get('sid'))
        gateway['family'] = 'aqara'
        list_devs.append(gateway)
        print('Find aquara devices')
        list_devs.append({'model': 'philips.light.candle', 'family': 'philips_light',
                          'token': '76b0a683c37406443a7056417926989a', 'sid': '235444403'})
        
        yedev = ye.discover()
        print('find yeelight devices')
        for bulb in yedev:
            d = yedev[bulb]
            # url = urlparse(d.get('location'))
            del d['location']
            d['sid'] = d.pop('id')
            d['support'].append('on')
            d['support'].append('off')
            d['family'] = 'yeelight'
            list_devs.append(d)
        
        print('find sonff devices')
        sdevs = sof.search()
        for sdev in sdevs:
            list_devs.append(sdevs[sdev])
        
        print('Find custom devices')
        list_devs.append({'cmd': 'report', 'model': 'clock',
                          'sid': 'clock', 'family': 'virtual'})
        
        list_devs.extend(sc)
        list_devs.append({'cmd': 'report', 'model': 'dallastemp',
                          'sid': 'dallasDS0', 'family': 'arduino'})
        
        list_devs.append({'cmd': 'report', 'model': 'rgbstrip',
                          'sid': 'rgb01', 'family': 'arduino'})
        
        tv = Bravia('192.168.10.5', macaddres='FC:F1:52:2A:9B:1E')
        
        list_devs.append({'cmd': 'write', 'model': tv.model,
                          'sid': tv.sid, 'family': 'tv',
                          'ip': '192.168.10.5',
                          'mac': 'FC:F1:52:2A:9B:1E'})
        return list_devs
    
    def get_scenes(self):
        scenes = list()
        with os.scandir('../scenes') as it:
            for entry in it:
                if entry.name.endswith('.py') and entry.is_file():
                    name = entry.name[:-3]
                    name = name.replace('_', ' ')
                    _scene = importlib.import_module(entry.name[:-3])
                    if isinstance(_scene, BaseAutomation):
                        model = 'automation'
                    else:
                        model = 'scene'
                    
                    scenes.append({'sid': entry.name[:-3],
                                   'name':name.title(),
                                   'place': '',
                                   'family': 'scenes',
                                   'model': model})
        return scenes

    def registering(self):
        self.clear_db()
        self.create_db()
        self.accessing_db()
        list_devs = self.dev_list()

        print('Registering device:')
        for d in list_devs:
            if not d or not d.get('sid'):
                continue
            if 'cmd' in d:
                del d['cmd']
            if 'data' in d:
                del d['data']
            sid = d.get('sid')
            if sid in self.names:
                d['name'] = self.names[sid]['name']
                d['place'] = self.names[sid]['place']
            print(f"\t {d.get('model')}  {d.get('sid')} {d.get('name')} in {d.get('place')}")
            self.devices[d.get('sid')] = d

    def add_config(self):
        if 'config' in self.srv:
            self.srv.delete('config')
        self.srv.create('config')
        self.config = self.srv.db('config')
            
        with open('config.json') as jconf:
            config = json.load(jconf)
            for c in config.get('config'):
                self.config.add(c)
            print('Config added')
    
    def add_residents(self):
        if 'residents' in self.srv:
            self.srv.delete('residents')
        self.srv.create('residents')
        self.residents = self.srv.db('residents')
        
        with open('residents.json') as jfile:
            residents = json.load(jfile)
            for c in residents.get('residents'):
                self.residents.add(c)
            print('Resident added')
        
        
    # def add_index(self):
    #     print(f"Creating index on device: {db.devices.create_index([('sid', TEXT)], unique=True)}")
    #     print(f"Creating index on device data: {db.devices_data.create_index([('sid', TEXT)], unique=True)}")
    
    def add_place(self):
        
        for d in self.devices:
            sid = d['sid']
            if sid in self.names:
                d['name'] = self.names[sid]['name']
                d['place'] = self.names[sid]['place']
                self.devices[sid] = d
                print(self.devices[sid]['place'])


if __name__ == '__main__':
    r = Register()
    r.registering()
    r.add_config()
    r.add_residents()
    # r.add_place()

