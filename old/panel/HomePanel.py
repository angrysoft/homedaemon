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
__version__ = '0.1'

from functools import wraps
import asyncio
import operator
from os import urandom
from hashlib import sha256
import subprocess
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# async def send_event(msg):
#     reader, writer = await asyncio.open_connection(db['config']['tcp']['ip'],
#                                                    db['config']['tcp']['port'])
#     writer.write(msg.encode())
#     await writer.drain()
#     data = await reader.read(100)
#     writer.close()
#     return 'ok'


# def login_required(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         # if 'admin' not in session:
#             # return redirect(url_for('login', next=request.url))
#         return func(*args, **kwargs)
#     return decorated_function

# www
class Cmd(BaseModel):
    cmd:str
    result: Optional[int]

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('admin.html', context={'request': request})


@app.post('/system')
async def system(cmd:Cmd):
    commands = {'restart-homed': ['systemctl', 'restart', 'homed.service'],
                'reboot': ['systemctl', 'reboot', '-i'],
                'poweroff': ['systemctl', 'poweroff', '-i']}
    ret:subprocess.CompletedProcess = subprocess.run(commands.get(cmd.cmd, ['echo', '1']))
    cmd.result = ret.returncode
    return cmd


# # ______Admin______ #
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = request.form['user']
#         password = request.form['passwd']
#         pwd = sha256(password.encode()).hexdigest()
#         if user == db['config']['panel'].get('user') and pwd == db['config']['panel'].get('password'):
#             session['admin'] = 'admin'
#             return request.args.get('next', '/admin')
#         else:
#             return 'ko'
#     elif request.method == 'GET':
#         return render_template('/login.html')


# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))


# @app.route('/config', methods=['GET', 'POST'])
# @login_required
# def admin_config():
#     if request.method == 'POST':
#         pass
#     elif request.method == 'GET':  
#         config = [d for d in db['config']]  
#         return render_template('config.html', config=config)


# @app.route('/devices')
# @login_required
# def admin_devices():
#     devs = [d for d in db['devices']]
#     return render_template('devices.html', devices=sorted(devs, key=operator.itemgetter('name')))

# @app.route('/system/restart', methods=['GET', 'POST'])
# def system_restart():
#     if request.method == 'GET':
#         return request.args.get('status', 'ooops something is wrong')
#     elif request.method == 'POST':
#         subprocess.call(['systemctl', 'restart', 'homed.service'])
#         # subprocess.call(['systemctl', 'restart', 'emperor.uwsgi.service'])
#         status = 'ok'
#         return redirect(f'/system/restart?status={status}')
    
    
# @app.route('/system/reboot', methods=['GET', 'POST'])
# def system_reboot():
#     if request.method == 'GET':
#         return request.args.get('status', 'ooops something is wrong')
#     elif request.method == 'POST':
#         subprocess.call(['systemctl', 'reboot', '-i'])
#         status = 'ok'
#         return redirect(f'/system/restart?status={status}')

