#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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
__copyright__ = 'Copyright 2014-2019 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.9'


from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from functools import wraps
import json
import asyncio
from pycouchdb import Server
import operator
from os import urandom
from hashlib import sha256
from time import sleep
app = Flask(__name__)


async def send_event(msg):
    reader, writer = await asyncio.open_connection(db['config']['tcp']['ip'],
                                                   db['config']['tcp']['port'])
    writer.write(msg.encode())
    await writer.drain()
    data = await reader.read(100)
    writer.close()
    return 'ok'


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

# www
@app.route('/')
def index():
    devs = [d for d in db['devices']]
    devs_data = dict()
    for dd in db['devices-data']:
        devs_data[dd.get('sid')] = dd
    return render_template('index.html', devices=sorted(devs, key=operator.itemgetter('name')), devdata=devs_data, scenses=[])


@app.route('/dev/config')
def dev_conf():
    ret = db['config'].get('websocket', {'ip': 'localhost', 'port': 9000})
    return json.dumps(ret)


@app.route('/dev/<sid>')
def dev(sid):
    ret = db['devices'].get(sid)
    return json.dumps(ret)


@app.route('/dev/data/<sid>')
def dev_data(sid):
    ret = db['devices-data'].get(sid)
    return json.dumps(ret)


@app.route('/dev/data/all')
def dev_data_all():
    device_data = list() 
    for d in db['devices-data']:
        device_data.append(d)
    return json.dumps(device_data)


@app.route('/dev/write', methods=['GET', 'POST'])
def dev_write():
    """Send"""
    if request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        msg = {'cmd': 'write',
               'model': request.form.get('model'),
               'sid': request.form.get('sid'),
               'data': {request.form.get('cmdname'): request.form.get('cmdvalue')}}
        asyncio.run(send_event(json.dumps(msg)))
    return redirect(f'/dev/write/?status=ok')


@app.route('/tv')
def tv_pilot():
    return render_template('tvpilot.html')


@app.route('/tv/button/<name>', methods=['GET', 'POST'])
def tv_button(name):
    """Send"""
    if request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        msg = {'cmd': 'write',
               'model': 'bravia',
               'sid': 'tv01',
               'data': {'button': name}}
        status = asyncio.run(send_event(json.dumps(msg)))
    return redirect('/tv/button/{}?status={}'.format(name, status))


@app.route('/devices')
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


# ______Admin______ #
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['passwd']
        pwd = sha256(password.encode()).hexdigest()
        if user == db['config']['user'].get('user') and pwd == db['config']['user'].get('password'):
            session['admin'] = 'admin'
            return request.args.get('next', '/admin')
        else:
            return 'ko'
    elif request.method == 'GET':
        return render_template('admin/login.html')


@app.route('/admin/logout')
def logout():
    # remove the username from the session if it's there
    # session.pop('username', None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin/admin.html')

@app.route('/admin/config', methods=['GET', 'POST'])
@login_required
def admin_config():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':  
        config = [d for d in db['config']]  
        return render_template('admin/config.html', config=config)


@app.route('/admin/devices')
@login_required
def admin_devices():
    devs = [d for d in db['devices']]
    return render_template('admin/devices.html', devices=sorted(devs, key=operator.itemgetter('name')))


# def connect_db():
#     db = None
#     for x in range(0,10):
#         try:
#             db = Server()
#             break
#         except ConnectionRefusedError:
#             sleep(1)
#     return db


# db = connect_db()
db = Server()
app.secret_key = urandom(24)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)
