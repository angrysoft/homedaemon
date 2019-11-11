#!/usr/bin/python

from pycouchdb import Server
import json

srv = Server()

with open('dump.json', 'r') as jfile:
    dbs = json.load(jfile)
    for dbname in dbs:
        srv.create(dbname)
        db = srv.db(dbname)
        for doc in dbs[dbname]:
            db.add(doc)
            

        