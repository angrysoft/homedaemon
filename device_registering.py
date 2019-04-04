#!/usr/bin/python3

from aquara import Gateway
from pymongo import MongoClient


cli = MongoClient()
db = cli.homedamondb

gw = Gateway()
for d in gw.read_all_devices():
    del d['cmd']
    data = d.get('data')
    del d['data']
    d.update(data)
    print(d)
