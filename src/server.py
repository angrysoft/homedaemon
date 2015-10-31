#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# server.py
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

import json
from flask import Flask
from flask import request
from flask import render_template
from threading import Thread
from time import sleep
import serial
import sys
import os
# import signal
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

    def loadConfig(self, configFile):
        """loadConfig"""
        self.data  = {}
        with open(configFile, 'r') as jdata:
            self.data = json.load(jdata)

    def nSort(self, l):
        """Sort list of digits and text"""
        digit = []
        text = []
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

    def getButton(self, btnname, func='On'):
        """buttonOn: get button on code and run sendCode"""
        if btnname in self.data:
            if func in self.data[btnname]:
                return self.data[btnname][func]

    def getAllButtons(self):
        """getButtons"""
        return self.nSort(list(self.data.keys()))


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

    def tescik(self):
        """tescik"""
        print('tescik sceny bla bla')

    def getAllScenes(self):
        """getAllScenes"""
        return self.scenes.keys()


class Commands(JsonConfig):
    """Class Commands"""

    def runCmd(self, cmd, state):
        """runCmd"""
        if cmd in self.data:
            if state in self.data[cmd]:
                return os.system(self.data[cmd][state])

    def getAllCommands(self):
        """getAllCommands"""
        return sorted(self.data.keys())


class Sensors(JsonConfig):
    """Class Sensors"""
    def getLight(self, num):
        """getLight"""
        if num in self.data['Light']:
            return self.data['Light'][num]

    def getTemp(self, num):
        """getTemp"""
        if num in self.data['Temp']:
            return self.data['Temp'][num]


class Controller(Thread):
    """docstring for SerialServer"""
    def __init__(self, serialPort, brate=9600):
        Thread.__init__(self)
        self.queue = Queue()
        self.answer = Queue()
        self.serialPort = serialPort
        self.baudrate = brate
        self.controller = None
        self.loop = True
        self.rf = RF433()
        self.scenes = Scenes('../scenes')
        self.color = Colors()
        self.commands = Commands()
        self.status = 'Not Connected'

    def __setup(self):
        """__setup"""
        self.scenes.loadScenes()
        self.rf.loadConfig('../files/rf433.json')
        # self.ir.loadConfig(self.config['ir_config'])
        self.color.loadConfig('../files/colors.json')
        self.commands.loadConfig('../files/commands.json')

    def __connect(self):
        """docstring for __connect"""
        while True:
            if os.path.exists(self.serialPort):
                self.controller = serial.Serial(port=self.serialPort, baudrate=9600)
                self.status = 'Connected'
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

    def checkConnection(self):
        """checkConnection"""
        self.writeSerial('ping')
        sleep(0.2)
        if self.readSerial() == 'pong':
            self.status = "Connected"
            return True
        else:
            self.status = "Not Connected"
            return False

    def sendRF(self, code):
        """docstring for sendRF"""
        self.writeSerial('W.{0}'.format(code))

    def parseCommand(self, cmd):
        """parseEvent"""
        print(cmd)
        if type(cmd) == tuple:
            if cmd[0] == 'scene':
                self.scenes.runScene(cmd[1])
            elif cmd[0] == 'button':
                self.sendRF(self.rf.getButton(cmd[1], cmd[2]))
            elif cmd[0] == 'ledRGB':
                self.writeSerial('F.{0}'.format(cmd[1]))
            elif cmd[0] == 'ledcolor':
                self.writeSerial('F.{0}'.format(self.color.getColor(cmd[1])))

    def run(self):
        """docstring for run"""
        self.__setup()
        self.__connect()

        while self.loop:
            # if not self.checkConnection():
            #    self.__connect()
            #    continue
            if self.queue.notEmpty():
                self.parseCommand(self.queue.pop())
            else:
                sleep(0.5)

    def close(self, *args):
        """docstring for close"""
        self.loop = False


@app.route('/')
def start_page():
    print('Hello World!')
    return render_template('index.html', status=ctrl.status)


@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
    """"""
    if request.method == 'POST':
        for button, func in request.args.items():
            ctrl.queue.put(('button', button, func))
        return 'ok'
    else:
        print('show buttons')
        return render_template('buttons.html', buttons=ctrl.rf.getAllButtons())


@app.route('/scenes', methods=['GET', 'POST'])
def scenes():
    """"""
    if request.method == 'POST':
        for sc in request.args.keys():
            ctrl.queue.put(('scene', sc))
        return 'ok'
    else:
        print('show scenes')
        return render_template('scenes.html', scenes=ctrl.scenes.getAllScenes())


@app.route('/leds', methods=['GET', 'POST'])
def leds():
    """led"""
    if request.method == 'POST':
        for color, val in request.args.items():
            if color == 'RGB':
                ctrl.queue.put(('ledRGB', val))
            elif color == 'name':
                ctrl.queue.put(('ledcolor', val))
        return 'ok'
    else:
        print('Led color')
        return render_template('leds.html', colors=ctrl.color.getAllColors())


@app.route('/commands', methods=['GET', 'POST'])
def commands():
    """"""
    if request.method == 'POST':
        for button, func in request.args.items():
            ctrl.queue.put(('command', cmd, func))
        return 'ok'
    else:
        print('show buttons')
        return render_template('commands.html', buttons=ctrl.commands.getAllCommands())

if __name__ == '__main__':
    ctrl = Controller('/dev/ttyACM0')
    ctrl.start()
    #signal.signal(signal.SIGINT, ctrl.close)
    #signal.signal(signal.SIGHUP, ctrl.close)
    #signal.signal(signal.SIGQUIT, ctrl.close)
    #signal.signal(signal.SIGTERM, ctrl.close)
    app.run(debug=True)
