#!/usr/bin/env python
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

__author__='Sebastian Zwierzchowski'
__copyright__='Copyright 2014 Sebastian Zwierzchowski'
__license__='GPL2'
__version__='0.1'

import getopt
import signal
import sys
import os
import socket
from threading import Thread
from time import sleep
import serial
import thread

import sys

#colors
black="\x1b[;30m"
red="\x1b[;31m"
green="\x1b[;32m"
yellow="\x1b[;33m"
blue="\x1b[;34m"
default="\x1b[;00m"
# end colors

class Config(dict):
    
    def __init__(self):
        # default value
        self['debug']   = "False"
        self['host']    = 'localhost'
        self['port']    = 9999
        self['bufsize'] = 1024
        self['serial']  = '/dev/ttyUSB0'
        
    
    def writeDefaultConfig(self,infile):
        """docstring for writeDefaultConfig"""
        with open(infile,'w') as f:
            for key in self.keys():
                f.write('{0} = {1}\n'.format(key,self[key]))
        return
                
    def loadFromFile(self,infile,sep='='):
        if not os.path.exists(infile):
            self.writeDefaultConfig(infile)
            return
            
        with open(infile,'r') as f:
            for line in f.readlines():
                if line.rfind(sep) == -1:
                    continue
                argv, value = line.split(sep,1)
                argv = argv.strip()
                if argv.rfind('#') == 0:
                    continue
                value = value.strip()
                value = value.strip('"')
                self[argv] = value
                
        return


class SmartHome:
    """docstring for SmartHome"""
    def __init__(self,configFile='SmartHome.conf'):
        self.queue = []
        self.config = Config()
        self.config.loadFromFile(configFile)
        self.loop = True
        self.controller = serial.Serial(port=self.config['serial'], baudrate=9600)
        
    def debug(self,msg):
        if self.config['debug'] == "False": return
        #colors
        green="\x1b[;32m"
        yellow="\x1b[;33m"
        default="\x1b[;00m"
        # end colors
        sys.stderr.write('%s>>> %sDEBUG: %s%s\n' % (green,yellow,default,msg))
    
    def runEvent(self,cmd):
        """docstring for runEvent"""
        cmd = cmd.strip()
        if cmd == '':return
        self.debug(cmd)
        
    def openSerial(self):
        """docstring for openSerial"""
        
        #reconnect is potential leek check this later or cpu 
        try:
            while self.controller.readable():
                print('is redable')
                self.queue.append(self.controller.readline())
        except:
            while True:
                if os.path.exists(self.config['serial']):
                    sleep(3)
                    self.controller = serial.Serial(port=self.config['serial'], baudrate=9600)
                    self.openSerial()
                
            
    def exit(self,status=0):
        """docstring for exit"""
        self.debug('exit status = {0}'.format(status))
        sys.exit(status)
    
    def start(self):
        """main loop"""
        thread.start_new_thread(self.openSerial,())
        while self.loop:
            if len(self.queue) > 0:
                self.runEvent(self.queue.pop())
            else:
                sleep(1)
    def stop(self,*args):
        """stop mainloop"""
        self.loop = False
            
        
def usage():
    print('{0} version : {1}'.format(os.path.basename(sys.argv[0]),__version__))
    print('usage : {0} [start|stop|restart]'.format(os.path.basename(sys.argv[0])))


def print_help():
    print('-h --help     : print help screen')
    print('-c --config   : path to config file')
    sys.exit(0)


if  __name__ == "__main__":
  
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(1)
    #change assert to somting better :) 
    
    for o,a in opts:
        if o in ("-h", "--help"):
            print_help()
        else:
            assert False, "unhandled option"
    
    if args == []:
        usage()
        sys.exit(1)
        
    srv = SmartHome()
    signal.signal(signal.SIGINT,srv.stop)
    signal.signal(signal.SIGHUP,srv.stop)
    signal.signal(signal.SIGQUIT,srv.stop)
    signal.signal(signal.SIGTERM,srv.stop)
    
    for a in args:
        if a == "start" :
                srv.start()
        elif a == "stop":
            srv.stop()
        else:
            assert False, "unhandled option"
            

        
    

