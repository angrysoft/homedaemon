#!/usr/bin/python3

from aquara import Gateway
from pymongo import TEXT, MongoClient
from pymongo.errors import DuplicateKeyError
from yeelight import Yeelight
from urllib.parse import urlparse

cli = MongoClient()
db = cli.homedaemondb


def clear_devs():
    print('Remove all device and device data')
    db.devices.drop()
    db.devices_data.drop()


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


def registering(list_devs):

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
        try:
            dev_id = db.devices.insert_one(d)
            dev_data_id = db.devices_data.insert_one(data)
        except DuplicateKeyError:
            print('\t  Device already exists skipping')


def add_index():
    print(f"Creating index on device: {db.devices.create_index([('sid', TEXT)], unique=True)}")
    print(f"Creating index on device data: {db.devices_data.create_index([('sid', TEXT)], unique=True)}")


if __name__ == '__main__':
    # result = db.devices_data.update_one({'sid': 'rgb01'}, {'$set': {'dupa': 'blada'}})
    clear_devs()
    registering(dev_list())
    add_index()
    # devs = [d for d in db.devices.find()]
    # print(devs)
