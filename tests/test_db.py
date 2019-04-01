#!/usr/bin/env python3

from angrysql.sqlitedb import Connection
from homedaemon.devicesdb import *

db = Connection({'dbfile': 'device.db'})
dev = Devices()