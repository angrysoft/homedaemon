#!/usr/bin/python

from pycouchdb import Server
import json


dblist = ('config',)#, 'devices', 'devices-data')
srv = Server()
dump = {}
for dbname in dblist:
    db = srv.db(dbname)
    dump[dbname] = []
    for doc in db:
        del doc['_rev']
        dump[dbname].append(doc)

with open('dump.json', 'w') as jfile:
    json.dump(dump, jfile)

        