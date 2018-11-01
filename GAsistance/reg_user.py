#!/usr/bin/python3

import json
from angrysql.sqlitedb import Connection
from oauth import Users

users = None
with open('users.json', 'r') as jfile:
    users = json.load(jfile)


db = Connection({'dbfile': 'db/users.db'})
db.create_tables(Users)

# for u in users:
#     user = Users()
#     user.google_client_id = u.get('google_client_id')
#     user.redirect_uri = u.get('redirect_uri')
#     user.google_client_secret = u.get('google_client_secret')
#     db.insert(user)
# db.commit()
user = db.select(Users).where(Users.google_client_id == 'johGha8w').first()
print(user.user_id)