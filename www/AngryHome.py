#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AngryHome.py
# Copyright (C) 2019 Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

__author__ = 'Sebastian Zwierzchowski'
__copyright__ = 'Copyright 2019 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.1'


from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import Response
from flask import stream_with_context
from functools import wraps
import json
from pycouchdb import Server
import operator
import jwt
from os import urandom
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
from utils import TcpWrite
import redis
from time import sleep
import logging
from gasistant import OAuth, Actions, WebHook

db = Server()
config = db.db('config')
tcp_config = config['tcp']['client']
tcp_config['secret'] = config['tcp']['secret']

app = Flask(__name__)

logging.basicConfig(filename='gast.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logging.warning('app starts')


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def devices():
    places = dict()
    items_list = sorted([d for d in db['devices']], key=operator.itemgetter('name'))
    for s in db['scenes']:
        if s.get('automatic') == False:
            s['model'] = 'scene'
            items_list.append(s)
    
    for item in items_list:
        place = item.get('place')
        if not place:
            continue
        if place not in places:
            places[place] = list()
        places[place].append(item)
    return render_template('devices.html', places=places)


@app.route('/scene/list')
def scenes_list():
    sc_list = list()
    for s in db['scenes']:
        if s.get('automatic') == False:
            sc_list.append(s)
    return json.dumps(sc_list)


@app.route('/dev/<sid>')
@login_required
def dev(sid):
    ret = db['devices'].get(sid)
    return json.dumps(ret)


@app.route('/dev/write', methods=['GET', 'POST'])
@login_required
def dev_write():
    if request.method == 'POST':
        tcp = TcpWrite(tcp_config['ip'], tcp_config['port'], tcp_config['secret'])
        tcp.writer(request.data)
        return redirect('/dev/write?status=ok')
    elif request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
 

@app.route('/dev/data/<sid>')
@login_required
def dev_data(sid):
    ret = db['devices-data'].get(sid)
    return json.dumps(ret)


@app.route('/dev/data/all')
@login_required
def dev_data_all():
    device_data = list() 
    for d in db['devices']:
        device_data.append({'model': d['model']}.update(db['devices-data'].get(d['sid'])))
    return json.dumps(device_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'userid' in session:
            return redirect('/')
        return render_template('login.html')
    elif request.method == 'POST':
        token = request.form.get('idtoken')
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, g_requests.Request(),
                                                  '185939031950-ofl3lt8mhuvl1tho2p0i308vqcum5reg.apps.googleusercontent.com')
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            # ID token is valid. Get the user's Google Account ID from the decoded token.
            
            try:
                if idinfo['sub'] in db['residents']:
                    session['userid'] = idinfo['sub']
                    session['locale'] = idinfo['locale']
                    session['picture'] = idinfo['picture']
                    session['name'] = idinfo['']
                    return 'ok'
                else:
                    return 'not_registred'
            except KeyError:
                return 'db error'
        except ValueError:
            return 'Invalid token'


@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

@app.route('/stream')
@login_required
def stream():
    return Response(event(), mimetype='text/event-stream', headers={'Cache-Control': 'no-cache',
                                                                    'Access-Control-Allow-Origin': '*',
                                                                    'Connection': 'keep-alive'})
@stream_with_context
def event():
    yield "data: hello\n\n"
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    channel = r.pubsub()
    channel.subscribe('msg')
    channel.get_message()
    while True:
        try:
            msg = channel.get_message()
            if msg:
                yield f'data: {msg.get("data")}\n\n'
        except redis.exceptions.ConnectionError:
            sleep(5)
        sleep(0.001)


### Google Asistant ###
@app.route('/auth')
def auth():
    """Auth"""
    if request.method == 'GET':
        logging.warning('auth get {}, {}'.format(request.args,
                                                         request.headers))
        url = '/auth'
        if request.args.get('response_type', '') == 'code':
            g_auth = OAuth(db)
            url = g_auth.auth(request.args)
            logging.warning(url)
        return render_template('auth.html', uri=url)


@app.route('/auth/token', methods=['POST'])
def token():
    """Token"""
    logging.warning('token post {}, {}'.format(request.form,
                                                       request.headers))
    g_auth = OAuth(db)
    status = 400
    data = '{"error": "invalid_grant"}'
    if request.form.get('grant_type') == 'authorization_code':
        status, data = g_auth.get_new_token(request.form)
    elif request.form.get('grant_type') == 'refresh_token':
        status, data = g_auth.refresh_token(request.form)
    elif request.form.get('grant_type') == 'urn:ietf:params:oauth:grant-type:jwt-bearer':
        pass

    logging.warning(f'token: {status}, {data}')

    return app.response_class(response=data,
                              status=status,
                              mimetype='application/json')


@app.route('/status', methods=['GET', 'POST'])
def status():
    """Status"""
    g_auth = OAuth(db)
    _response = ''
    _status = 200
    if request.method == 'GET':
        logging.warning('status get {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        return request.args.get('status', 'ooops something is wrong')

    elif request.method == 'POST':
        logging.warning('status post {}, {}'.format(request.data, request.headers.get('Authorization')))

        if g_auth.log_by_token(request.headers.get('Authorization', '')):
            g_action = Actions(request.data)
            if g_action.intent == 'action.devices.EXECUTE':
                cmd = g_action.execute()
                logging.warning(f'{cmd}')
                tcp = TcpWrite(tcp_config['ip'], tcp_config['port'], tcp_config['secret'])
                tcp.writer(cmd)
            _response = g_action.response
        else:
            _response = '{"error":"user_not_found"}'
            _status = 401
        logging.warning(f'{_response}')
        return app.response_class(response=_response,
                                  status=_status,
                                  mimetype='application/json')


@app.route('/home/status', methods=['GET', 'POST'])
def home_status():
    """Status"""
    if request.method == 'GET':
        logging.warning('status get {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        return request.args.get('status', 'ooops something is wrong')

    elif request.method == 'POST':
        _response = ''
        _status = 200
        _data = json.loads(request.data)
        logging.warning(f'{_data}')
        webhook = WebHook(_data)
        _response = webhook.response()
        return app.response_class(response=_response,
                                  status=_status,
                                  mimetype='application/json')

app.secret_key = urandom(24)

app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax')

if __name__ == '__main__':
    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax')
    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)
