#!/usr/bin/python3

from pyiot.xiaomi.aqara import Gateway
from pyiot.xiaomi.yeelight import Yeelight
from pyiot.sony import Bravia
from pyiot.sonoff import Discover
from urllib.parse import urlparse
import importlib
importlib.sys.path.append('../')
importlib.sys.path.append('../scenes')
from homedaemon.scenes import BaseAutomation, BaseScene
import json
import os
import sys


class Devs:
    def __init__(self, devs_path):
        self.devices = []
        self.devices_data = None
        self.config = None
        self.residents = None
        self.dev_path = devs_path
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
    
    def discover(self):
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
            d = sdevs[sdev]
            d['family'] = 'sonoff'
            d['sid'] = d.pop('id')
            list_devs.append(d)
        
        print('Find custom devices')
        list_devs.append({'model': 'clock',
                          'sid': 'clock', 'family': 'virtual'})
        
        list_devs.extend(sc)
        list_devs.append({'model': 'dallastemp',
                          'sid': 'dallasDS0', 'family': 'arduino'})
        
        list_devs.append({'model': 'rgbstrip',
                          'sid': 'rgb01', 'family': 'arduino'})
        
        tv = Bravia('192.168.10.5', macaddres='FC:F1:52:2A:9B:1E')
        
        list_devs.append({'cmd': 'write', 'model': tv.model,
                          'sid': tv.sid, 'family': 'tv',
                          'ip': '192.168.10.5',
                          'mac': 'FC:F1:52:2A:9B:1E'})
        for _dev in list_devs:
            sid = _dev.get('sid')
            if sid:
                if sid in self.names:
                    _dev['name'] = self.names[sid]['name']
                    _dev['place'] = self.names[sid]['place']
                
                self.devices.append({'family': _dev.get('family'),
                                  'name':   _dev.get('name'),
                                  'sid':    _dev.get('sid'),
                                  'model':  _dev.get('model'),
                                  'place':  _dev.get('place')})
    
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

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        dev = Devs('devs')
        dev.discover()
        for _dev in dev.devices:
            with open(f"{sys.argv[1]}/{_dev.get('sid')}.json", "w") as jfile:
                json.dump(_dev, jfile, indent=4, sort_keys=True)