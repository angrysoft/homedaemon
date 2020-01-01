import json
import secrets
from datetime import datetime
from pycouchdb import DatabaseError


class OAuth:
    def __init__(self, srv):
        self.srv = srv
        self.usersdb = self._get_db('google-users')
        self.codesdb = self._get_db('google-codes')
        self.tokendb = self._get_db('google-token')
        self.codes = dict()
        
    def _get_db(self, dbname):
        if dbname not in self.srv:
            self.srv.create(dbname)
        return self.srv.db(dbname)

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
        user_id = self.verify_client_secret(args.get('client_id', ''), args.get('client_secret', ''))
        if not user_id:
            err = 'user_id'
        elif self.verify_code(user_id, args.get('code', '')):
            err = 'user_code'

        if user_id and self.verify_code(user_id, args.get('code', '')):
            self.tokendb.delete(user_id)
            token = {'_id': user_id,
                     'user_id': user_id,
                     'token_type': 'Bearer',
                     'access_token': self._token(20),
                     'refresh_token': self._token(20),
                     'expires_in': 3600}

            self.tokendb.add(token)
            return 200, json.dumps({
                "token_type": token.token_type,
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "expires_in": token.expires_in})

        return 400, json.dumps({"error": "invalid_grant", "erro_msg": f"{err}"})

    def refresh_token(self, args):
        err = None
        user_id = self.verify_client_secret(args.get('client_id', ''), args.get('client_secret', ''))
        if user_id:
            token = self.tokensdb.get(user_id)
            if token and token['refresh_token'] == args.get('refresh_token'):
                token['access_token'] = self._token(20)
                self.tokendb[user_id] = token
                return 200, json.dumps({
                    "token_type": token.token_type,
                    "access_token": token.access_token,
                    "expires_in": token.expires_in})
            else:
                err = 'token'
        else:
            err = 'user_id'

        return 400, json.dumps({"error": "invalid_grant", "erro_msg": f"{err}"})

    def log_by_token(self, auth):
        if auth.find(' ') > 0:
            token_type, token = auth.split(' ', 1)
            try:
                # user_token = self.db.select(Tokens).where(Tokens.access_token == token).first()
                user_token = self.tokendb.find(selctor={'acces_token': token}, limit=1)[0]
                if user_token:
                    return True
            except DatabaseError as err:
                return False
        return False

    def verify_code(self, user_id, code):
        times = int(datetime.now().timestamp())
        user_code = self.codesdb.get(user_id, {})
        if user_code.get('code') == code and (times <= int(user_code['expire'])):
            return True
        return False

    def verify_redirect_uri(self, client_id, redirect_uri):
        # user = self.db.select(Users).where(Users.google_client_id == client_id).first()
        user = self.usersdb.get(client_id)
        if user and user.get('redirect_uri') == redirect_uri:
            return user.user_id
        return None

    def verify_client_secret(self, client_id, client_secret):
        # user = self.db.select(Users).where(Users.google_client_id == client_id).first()
        user = self.usersdb.get(client_id)
        if user and user.get('client_secret') == client_secret:
            return user.user_id
        return None

    def gen_code(self, user_id, expire=600):
        self.codesdb.delete(user_id)
        new_code = self._token()
        new_user_code = {
            '_id': user_id,
            'user_id': user_id,
            'code': self._token(),
            'expire': int(datetime.now().timestamp()) + expire
        }
        self.codesdb.add(new_user_code)
        return new_user_code['code']

    def json_token(self, exipire=3600):
        pass

    def is_signed(self, client_id):
        pass

    @staticmethod
    def _token(size=10):
        return secrets.token_urlsafe(size)
