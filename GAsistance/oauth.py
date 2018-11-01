import json
import secrets
from datetime import datetime
from angrysql.sqlitedb import Connection
from angrysql import BaseModel, Column, Integer, String


class Users(BaseModel):
    user_id = Column(Integer(), primary_key=True)
    google_client_id = Column(String(), unique=True, nullable=False)
    google_client_secret = Column(String(), nullable=False)
    redirect_uri = Column(String(),nullable=False)
    signed = Column(Integer(), default=0)


class Codes(BaseModel):
    code_id = Column(Integer(), primary_key=True)
    code = Column(String())
    expire = Column(Integer())
    user_id = Column(Integer(), nullable=False, foreignkey='users.user_id')


class Tokens(BaseModel):
    token_id = Column(Integer(), primary_key=True)
    token_type = Column(String(255), default='Bearer')
    access_token = Column(String())
    refresh_token = Column(String())
    expires_in = Column(Integer(), default=3600)
    user_id = Column(Integer(), nullable=False, foreignkey='users.user_id')


class OAuth:
    def __init__(self):
        self.db = Connection({'dbfile': 'db/users.db'}, echo=True)
        self.db.create_tables(Users, Codes)
        self.codes = dict()

    def auth(self, args):
        url = '/user.html'
        user_id = self.verify_redirect_uri(args.get('client_id', ''), args.get('redirect_uri', ''))
        if user_id:
            code = self.gen_code(user_id)
            url = '{}?code={}&state={}'.format(args.get('redirect_uri', '/user.html'),
                                               code,
                                               args.get('state'))
        return url

    def get_new_token(self, args):
        user_id = self.verify_client_secret(args.get('client_id', ''), args.get('redirect_uri', ''))
        if user_id and self.verify_code(user_id, args.get('code', '')):
            self.db.delete(Tokens).where(Tokens.user_id == user_id).all()
            token = Tokens()
            token.access_token = self._token(20)
            token.refresh_token = self._token(20)
            self.db.insert(token)
            self.db.commit()
            return 200, json.dumps({
                "token_type": token.token_type,
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "expires_in": token.expires_in})

        return 400, '{"error": "invalid_grant"}'

    def refresh_token(self, args):
        user_id = self.verify_client_secret(args.get('client_id', ''), args.get('redirect_uri', ''))
        if user_id:
            token = self.db.select(Tokens).where(Tokens.user_id == user_id).first()
            if token and token.refresh_token == args.get('refresh_token'):
                token.access_token = self._token(20)
                self.db.update(token).where(Tokens.user_id == user_id)
                self.db.commit()
                return 200, json.dumps({
                    "token_type": token.token_type,
                    "access_token": token.access_token,
                    "expires_in": token.expires_in})

        return 400, '{"error": "invalid_grant"}'

    def verify_code(self, user_id, code):
        times = int(datetime.now().timestamp())
        user_code = self.db.select(Codes).where(Codes.user_id == user_id).first()
        if user_code.code == code and (times <= int(user_code.expire)):
            return True
        return False

    def verify_redirect_uri(self, client_id, redirect_uri):
        user = self.db.select(Users).where(Users.google_client_id == client_id).first()
        if user and user.redirect_uri == redirect_uri:
            return user.user_id
        return None

    def verify_client_secret(self, client_id, client_secret):
        user = self.db.select(Users).where(Users.google_client_id == client_id).first()
        if user and user.google_client_secret == client_secret:
            return user.user_id
        return None

    def gen_code(self, user_id, expire=600):
        user_code = self.db.select(Codes).where(Codes.user_id == user_id).first()
        new_code = self._token()
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
    def _token(size=10):
        return secrets.token_urlsafe(size)

    def __del__(self):
        self.db.conn.close()
