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
from functools import wraps
import json
from pycouchdb import Server
import operator
import jwt
from os import urandom
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
from utils import TcpRead, TcpWrite
from threading import Thread
from time import sleep

db = Server()
config = db.db('config')
tcp_config = config['tcp']['client']
tcp_config['secret'] = config['tcp']['secret']

app = Flask(__name__)


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

# www
@app.route('/')
@login_required
def index():
    devs = [d for d in db['devices']]
    devs_data = dict()
    for dd in db['devices-data']:
        devs_data[dd.get('sid')] = dd
    return render_template('index.html', devices=sorted(devs, key=operator.itemgetter('name')), devdata=devs_data, scenses=[])


# @app.route('/dev/config')
# @login_required
# def dev_conf():
#     ret = db['config']['websocket']
#     config = {'urltoken': ret['urltoken'],
#               'secret': jwt.encode({'api':'1.0', 'client': 'browser'}, ret['secret'], algorithm='HS256').decode(),
#               'internet': ret['internet'],
#               'localnetwork': ret['localnetwork']}
#     config.update(ret['webserver'])
#     return json.dumps(config)


@app.route('/scenes/list')
def scenes_list():
    return ''


@app.route('/dev/<sid>')
@login_required
def dev(sid):
    ret = db['devices'].get(sid)
    return json.dumps(ret)


@app.route('/dev/write', methods=['GET', 'POST'])
@login_required
def dev_write():
    tcp = TcpWrite(tcp_config['ip'], tcp_config['port'], tcp_config['secret'])
    tcp.writer(request.data)
    return 'ok'


@app.route('/dev/data/<sid>')
@login_required
def dev_data(sid):
    ret = db['devices-data'].get(sid)
    return json.dumps(ret)


@app.route('/dev/data/all')
@login_required
def dev_data_all():
    device_data = list() 
    for d in db['devices-data']:
        d['model'] = db['devices'][d['sid']]['model']
        device_data.append(d)
    return json.dumps(device_data)


@app.route('/devices')
@login_required
def devices():
    devs = sorted([d for d in db['devices']], key=operator.itemgetter('name'))
    sc_list = list()
    for s in db['config']['scenes_list']['list']:
        if not s.get('automaitc'):
            sc_list.append(s)
    return render_template('devices.html',
                           devices=devs,
                           websock=db['config']['websocket']['ip'],
                           wp=db['config']['websocket']['port'],
                           scenes=sc_list)


@app.route('/tv')
@login_required
def tv():
    return render_template('tvpilot.html')


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
            print(f"{idinfo['sub']}\n{db['config']['users']['gusers']} \n {session}")
            
            try:
                if idinfo['sub'] in db['config']['users']['gusers']:
                    session['userid'] = idinfo['sub']
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

def event():
    yield "data: hello\n\n"
    tcp = TcpRead(tcp_config['ip'], tcp_config['port'], tcp_config['secret'])
    for msg in tcp.reader():
        yield f'data: {msg}\n\n'


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
