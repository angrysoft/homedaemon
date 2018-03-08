#!/usr/bin/python
# -*- coding: utf-8 -*-
# jsonconfigs.py
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

import os
import sys
import json

__all__ = ['JsonConfig', 'RF433', 'Sensors']

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
            if but.get('alias'):
                name = but.get('alias')
            else:
                name = b
            onCode = but.get('On')
            offCode = but.get('Off')
            buttons.append({'name': name,
                            'on': onCode,
                            'off': offCode
                            })
        return buttons


class Scenes:
    """Class Scenes"""

    def __init__(self, scneDirectory):
        """Constructor for Scenes"""
        self.sceneDir = scneDirectory
        self.scenes = dict()

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


if __name__ == '__main__':
    rf = RF433()
    rf.loadConfig('../files/rf433.json')
    print(rf.getAllButtons())
