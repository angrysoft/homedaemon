#!/usr/bin/python3

from aquara import Gateway
from pymongo import TEXT, MongoClient
from pymongo.errors import DuplicateKeyError

cli = MongoClient()
db = cli.homedaemondb


def clear_devs():
    print('Remove all device and device data')
    db.devices.drop()
    db.devices_data.drop()


def dev_list():
    gw = Gateway()
    list_devs = gw.read_all_devices()
    list_devs.append({'cmd': 'report', 'model': 'dallastemp',
                      'sid': 'dallasT1', 'data': {'temp': 0}})
    list_devs.append({'cmd': 'report', 'model': 'rgbstrip', 'sid': 'rgb01',
                      'data': {'red': 0, 'green': 0, 'blue': 0}})
    list_devs.append({'cmd': 'report', 'model': 'bslamp1',
                      'sid': '0x000000000545b741',
                      'data': {'power': 'off'}})
    list_devs.append({'cmd': 'report', 'model': 'color',
                      'sid': '0x0000000007e7bae0',
                      'data': {'power': 'off'}})

    return list_devs


def registering(list_devs):

    print('Registering device:')
    for d in list_devs:
        del d['cmd']
        data = d.get('data')
        del d['data']
        data['sid'] = d.get('sid')
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
