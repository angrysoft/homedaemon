#!/usr/bin/python

from pycouchdb import Server
import json

srv = Server()

with open('dump.json', 'r') as jfile:
    dbs = json.load(jfile)
    for dbname in dbs:
        if dbname in srv:
            print(f'Db {dbname} exist spikping....')
            continue
        srv.create(dbname)
        db = srv.db(dbname)
        print(f'Restoring {dbname}')
        for doc in dbs[dbname]:
            db.add(doc)
    