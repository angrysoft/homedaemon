#!/usr/bin/env python3

from couchdb import Server


server = Server()
dev = server['devices']
devd = server['devices-data']

for d in dev:
    print(d, dev.get(d))

devices_data = dict()
for dd in devd:
    devices_data[dd] = devd[dd]

print(devices_data)
