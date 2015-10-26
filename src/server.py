#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SmartHouse.py
# Copyright (C) 2015  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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

import json
from flask import Flask
from flask import request
from flask import render_template
from threading import Thread
from time import sleep
import serial
import sys
import os
from random import randint

app = Flask(__name__)

class Queue:
    """Queue fifo list"""
    def __init__(self):
        self.q = []

    def put(self, arg):
        """put arg on end of list"""
        self.q.insert(0, arg)

    def pop(self):
        """pop"""
        return self.q.pop()

    def len(self):
        """len return size of queue"""
        return len(self.q)

    def notEmpty(self):
        """notEmpty"""
        if len(self.q) > 0:
            return True
        else:
            return False


class JsonConfig():
    """Class JsonConfig"""

    def __init__(self):
        """Constructor for JsonConfig"""
        self.data = {}

    def loadConfig(self,configFile):
        """loadConfig"""
        self.data  = {}
        with open(configFile, 'r') as jdata:
            self.data = json.load(jdata)


class RF433(JsonConfig):
    """Class RF433 send rf Code"""

    def getButton(self, btnname, func='On'):
        """buttonOn: get button on code and run sendCode"""
        if btnname in self.data:
            if func in self.data[btnname]:
                return self.data[btnname][func]

    def getAllButtons(self):
        """getButtons"""
        return sorted(list(self.data.keys()))


class Colors(JsonConfig):
    """Class Colors"""

    def getColor(self, colorName, dimmer=100):
        """color"""
        if colorName in self.data:
            return self.data[colorName]

    def getRandomColor(self):
        """randomColor"""
        lc = list(self.data)
        return self.getColor(lc[randint(0, len(lc)-1)])

    def getAllColors(self):
        """getAllColors"""
        ret = {}
        for x in self.data:
            ret[x] =  self.data[x].replace('.', ',')
        return ret


class Scenes:
    """Class Scenes"""

    def __init__(self, scneDirectory):
        """Constructor for Scenes"""
        self.sceneDir = scneDirectory
        self.scenes = {}

    def loadScenes(self):
        """loadScenes"""
        for s in os.listdir(self.sceneDir):
            if s.endswith('.sc'):
                print('Load scene: {0}'.format(s))
                with (open(os.path.join(self.sceneDir, s), 'r')) as f:
                    self.scenes[s.rsplit('.', 1)[0]] = f.read()

    def runScene(self, scene):
        """runScene"""
        if scene in self.scenes:
            try:
                exec(self.scenes[scene])
            except:
                sys.stderr.write('Run scene : {0} : failure'.format(scene))

    def getAllScenes(self):
        """getAllScenes"""
        return self.scenes.keys()


class Controller(Thread):
    """docstring for SerialServer"""
    def __init__(self, queue, serialPort, brate=9600):
        Thread.__init__(self)
        self.queue = queue
        self.serialPort = serialPort
        self.baudrate = brate
        self.controller = None
        self.loop = True
        self.rf = RF433()
        self.scenes = Scenes('../scenes')
        self.color = Colors()

    def __setup(self):
        """__setup"""
        self.scenes.loadScenes()
        self.rf.loadConfig('../files/rf433.json')
        # self.ir.loadConfig(self.config['ir_config'])
        self.color.loadConfig('../files/colors.json')
        # self.command.loadConfig(self.config['commands_config'])

    def __connect(self):
        """docstring for __connect"""
        while True:
            if os.path.exists(self.serialPort):
                self.controller = serial.Serial(port=self.serialPort, baudrate=9600)
                break
            sleep(3)

    def readSerial(self):
        """docstring for openSerial"""
        try:
            if self.controller.readable():
                data = self.controller.readline()
                data = data.decode()
                data = data.rstrip()
                return data
        except:
            pass

    def writeSerial(self, data):
        """docstring for writeSerial"""
        if self.controller.writable():
            data = '{0}\n'.format(data)
            self.controller.write(bytearray(data, 'ascii'))

    def sendRF(self, code):
        """docstring for sendRF"""
        self.writeSerial('W.{0}'.format(code))

    def parseEvent(self, e):
        """parseEvent"""
        print(e)

    def run(self):
        """docstring for run"""
        self.__setup()
        self.__connect()

        while self.loop:
            if self.queue.notEmpty():
                self.parseEvent(self.queue.pop())
            else:
                sleep(1)

    def close(self):
        """docstring for close"""
        self.loop = False

    def pushButton(self, b, f):
        """push_button"""
        print("set {0} {1}".format(b, f))
        print(self.rf.getButton(b, f))

    def runScene(self, sc):
        """runSecene"""
        print("Run scen {0}".format(sc))
        self.scenes.runScene(sc)

    def setLedRGB(self, rgb):
        """setLedRGB"""
        print(rgb)

    def setLedColor(self, cn):
        print(self.color.getColor(cn))


@app.route('/')
def start_page():
    print('Hello World!')
    return render_template('index.html')


@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
    """"""
    if request.method == 'POST':
        for button, func in request.args.items():
            ctrl.pushButton(button, func)
        return 'ok'
    else:
        print('show buttons')
        return render_template('buttons.html', buttons=ctrl.rf.getAllButtons())


@app.route('/scenes', methods=['GET', 'POST'])
def scenes():
    """"""
    if request.method == 'POST':
        for sc in request.args.keys():
            ctrl.runScene(sc)
        return 'ok'
    else:
        print('show scenes')
        return render_template('scenes.html', scenes=ctrl.scenes.getAllScenes())


@app.route('/leds', methods=['GET', 'POST'])
def leds():
    """led"""
    if request.method == 'POST':
        for color, val in request.args.items():
            print(color, val)
            if color == 'RGB':
                ctrl.setLedRGB(val)
            elif color == 'name':
                ctrl.setLedColor(val)
        return 'ok'
    else:
        print('Led color')
        return render_template('leds.html', colors=ctrl.color.getAllColors())

if __name__ == '__main__':

    q = Queue()
    ctrl = Controller(q, '/dev/ttyACM0')
    ctrl.start()
    app.run(debug=True)
