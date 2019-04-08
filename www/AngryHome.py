#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SmartHouse.py
# Copyright (C) 2014  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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
__version__ = '0.5'


from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import json
import asyncio
from pymongo import MongoClient

app = Flask(__name__)


async def send_event(msg):
    reader, writer = await asyncio.open_connection('127.0.0.1', 6666)
    writer.write(msg.encode())
    await writer.drain()
    # await asyncio.sleep(1)
    data = await reader.read(100)
    writer.close()
    return 'ok'


# www
@app.route('/')
def index():
    devices = [d for d in db.devices.find()]
    return render_template('index.html', devices=devices)


@app.route('/dev/<sid>')
def dev(sid):
    return db.devices.find_one({'sid': sid})


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


@app.route('/leds')
def leds():
    """led"""
    return render_template('leds.html')


@app.route('/leds/color/<num>')
def ledsColor(num):
    """led"""

    return db.getColor(num)


@app.route('/leds/pilot')
def leds_pilot():
    return render_template('ledpilot.html')


@app.route('/leds/changeColor/<rgb>', methods=['GET', 'POST'])
def changeColor(rgb):
    """changeColor"""
    if request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        msg = {'cmd': 'write',
               'model': 'ledstrip',
               'sid': 0,
               'data': {'rgb': rgb}}
        status = 'ok'
        asyncio.run(send_event(json.dumps(msg)))
    return redirect('/leds/changeColor/{}?status={}'.format(rgb, status))


cli = MongoClient()
db = cli.homedaemondb

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)
