import json
import os
import secrets
from datetime import datetime
from angrysql.sqlitedb import Connection
from angrysql import BaseModel, Column, Integer, String


class Users(BaseModel):
    user_id = Column(Integer(), primary_key=True)
    google_user_id = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    email = Column(String(255), unique=True)
    home_uri = Column(String())
    refresh_token = Column(String())
    signed = Column(Integer(), default=0)


class Codes(BaseModel):
    code_id = Column(Integer(), primary_key=True)
    code = Column(String())
    user_id = Column(Integer())
    expire = Column(Integer())


class OAuth:
    def __init__(self):
        self.db = Connection({'dbfile': 'db/users.db'}, echo=True)
        self.db.create_tables(Users, Codes)
        self.codes = dict()

    def auth(self, args):
        user = self.db.select(Users).where(Users.google_user_id == args.get('client_id', '')).first()
        url = '/user.html'
        if user and user.home_uri == args.get('redirect_uri', ''):
            code = self.gen_code(user.user_id)
            url = '{}?code={}&state={}'.format(code, args.get('state'))
        return url

    def gen_code(self, user_id, expire=600):
        user_code = self.db.select(Codes).where(Codes.user_id == user_id).first()
        new_code = self.token()
        time2expire = int(datetime.now().timestamp()) + expire

        if user_code:
            user_code.code = new_code
            user_code.expire = time2expire
            self.db.update(user_code).where(Codes.user_id == user_id).all()
        else:
            new_user_code = Codes()
            new_user_code.code = new_code
            new_user_code.expire = time2expire
            self.db.insert(new_user_code)
        self.db.commit()
        return new_code

    def json_token(self, exipire=3600):
        pass

    def is_signed(self, client_id):
        pass

    @staticmethod
    def token(size=10):
        return secrets.token_urlsafe(size)

    def __del__(self):
        self.db.conn.close()
