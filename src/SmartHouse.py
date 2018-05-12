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
import json

app = Flask(__name__)

class JsonConfig():
    """Class JsonConfig"""

    def __init__(self):
        """Constructor for JsonConfig"""
        self.data = dict()

    def loadConfig(self, configFile):
        """loadConfig"""
        self.data.clear()
        with open(configFile, 'r') as jdata:
            self.data = json.load(jdata)

    def get(self, key):
        """get"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def nSort(self, l):
        """Sort list of digits and text"""
        digit = list()
        text = list()
        for i in l:
            if i.isdigit():
                digit.append(i)
            else:
                text.append(i)
        digit.sort(key=int)
        text.sort()
        digit.extend(text)
        return digit


class RF433(JsonConfig):
    """Class RF433 send rf Code"""

    def getBtnByName(self, btnname, func='On'):
        """getButton: return button code"""
        if str(btnname) in self.data:
            func = func.capitalize()
            if func in self.data[btnname]:
                return self.data[btnname][func]

    def getAllButtons(self):
        """getButtons"""
        buttons = list()
        for b in self.nSort(list(self.data)):
            but = self.data.get(b)
            name = but.get('alias', b)
            onCode = but.get('On')
            offCode = but.get('Off')
            buttons.append({'name': name,
                            'on': onCode,
                            'off': offCode
                            })
        return buttons


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


@app.route('/rf/pilot')
def rfPilot():
    return render_template('rfpilot.html', buttons=rf.getAllButtons())


@app.route('/rf/pilot/button/<no>', methods=['GET', 'POST'])
def rfButton(no):
    """rfSend"""
    if request.method == 'GET':
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        print(rf.getBtnByName('1', func=request.args.get('func', 'On')))
        code = rf.getBtnByName(no, func=request.args.get('func', 'On'))
        print(no, request.args.get('func'), code)
        status = sendEvent('rf:{}'.format(code))
    return redirect('/rf/pilot/button/{}?status={}'.format(no, status))


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


@app.route('/temp/<number>')
def getTemp(number):
    """getTemp"""
    sendEvent('temp:{}'.format(number))
    return 'ok'


@app.route('/light/<number>')
def getLight(number):
    """getTemp"""
    sendEvent('light:{}'.format(number))
    return 'ok'


rf = RF433()
rf.loadConfig('/etc/smarthouse/rf433.json')

if __name__ == '__main__':


    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)
