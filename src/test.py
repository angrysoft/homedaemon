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

# import serial
#
# import serial
# ser = serial.Serial('/dev/ttyUSB0')  # open serial port
# print(ser.name)         # check which port was really used
# ser.write(b'F)     # write a string
# ser.close()
from event import Rf
from event import RGB

r = Rf(config='../files/rf433.json')
print(r.on('1'))
print(r.on('Salon Lampka'))

rgb = RGB()
rgb.red = 255
rgb.green = 50
rgb.blue = 100
rgb.dimmer = 250
print(rgb.red, rgb.green, rgb.blue)
# rgb.green = '10'
print(rgb.color())