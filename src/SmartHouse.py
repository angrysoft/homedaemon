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
__copyright__ = 'Copyright 2014 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.4'


from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import socket
import os
from jsonconfigs import RF433, Colors

app = Flask(__name__)


def sendEvent(msg, socketFile='/tmp/housed.sock'):
    if os.path.exists(socketFile):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        client.connect(socketFile)
        client.send(msg.encode('utf-8'))
        client.close()
        return 'ok'
    else:
        return 'ko'


# www
@app.route('/')
def index():
    print('Hello World!')
    return render_template('index.html', status='brak')


@app.route('/rf')
def buttons():
    """"""
    return render_template('rf.html', buttons=rf.getAllButtons())


@app.route('/rf/send/<code>', methods=['GET', 'POST'])
def rfSend(code):
    """rfSend"""
    if request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        status = sendEvent('rf:{}'.format(code))
    return redirect('/rf/send/{}?status={}'.format(code, status))


@app.route('/leds')
def leds():
    """led"""
    return render_template('leds.html')


@app.route('/leds/changeColor/<rgb>', methods=['GET', 'POST'])
def changeColor(rgb):
    """changeColor"""
    if request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        status = sendEvent('rgb:{}'.format(rgb))
    return redirect('/leds/changeColor/{}?status={}'.format(rgb, status))


if __name__ == '__main__':
    rf = RF433()
    rf.loadConfig('../files/rf433.json')
    col = Colors()
    col.loadConfig('../files/colors.json')

    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)
