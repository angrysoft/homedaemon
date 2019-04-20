#!/usr/bin/env python3

from pymongo import MongoClient


cli = MongoClient()
db = cli.homedaemon
dev = db.devices_data
for c in db.collection.watch():
    print(c)
    
