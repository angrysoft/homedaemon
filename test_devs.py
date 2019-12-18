#!/usr/bin/python

from pycouchdb import Server
from homedaemon.devices import Devices

devs = Devices()
srv = Server()
db = srv.db('devices')


for dev in db:
    devs.load(dev)