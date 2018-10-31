import json
import os
import secrets
from angrysql.sqlitedb import Connection
from angrysql import BaseModel, Column, Integer, String


class Users(BaseModel):
    user_id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    email = Column(String(255))
    user_info_id = Column(Integer())


class Auth:
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            raise FileExistsError('Config is missing: {}'.format(config_file))

        with open(config_file, 'r') as jdata:
            self.config = json.load(jdata)

        self.db = Connection(self.config)
            
    def json_token(self, exipire=3600):
        pass

    def verify_client_info(self, client_id, redirect_uri):
        pass

    def is_signed(self, client_id):
        pass

    @staticmethod
    def token(size=10):
        return secrets.token_urlsafe(size)
