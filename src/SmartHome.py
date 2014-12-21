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

__author__='Sebastian Zwierzchowski'
__copyright__='Copyright 2014 Sebastian Zwierzchowski'
__license__='GPL2'
__version__='0.2'

import getopt
import signal
import os
import socket
from threading import Thread
from time import sleep
import serial
import sys
import json
from random import randint


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


class Config(dict):
    
    def __init__(self):
        # default value
        self['debug'] = "False"
        self['host'] = 'localhost'
        self['port'] = '9999'
        self['bufsize'] = '1024'
        self['serial'] = '/dev/ttyUSB0'
        self['scenedir']= '/etc/SmartHome/Scenes'
        self['rf_config'] = '/etc/SmartHome/rf433.json'
        self['ir_config'] = '/ect/SmartHome/IR.json'
        self['colors_config'] = '/etc/SmartHome/colors.json'
        self['commands_config'] = '/etc/SmartHome/commands.json'

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

    def getKey(self, key):
        """getKey"""
        if key in self:
            return self[key]


class Scenes:
    """Class Scenes"""

    def __init__(self,scneDirectory):
        """Constructor for Scenes"""
        self.sceneDir = scneDirectory
        self.scenes = {}

    def loadScenes(self):
        """loadScenes"""
        for s in os.listdir(self.sceneDir):
            if s.endswith('.sc'):
                print('Load scene: {0}'.format(s))
                with (open('{0}/{1}'.format(self.sceneDir, s), 'r')) as f:
                    self.scenes[s.rsplit('.', 1)[0]] = f.read()

    def runScene(self, scene):
        """runScene"""
        if scene in self.scenes:
            exec(self.scenes[scene])


class RF433(JsonConfig):
    """Class RF433 send rf Code"""

    def buttonOn(self, btnname):
        """buttonOn: get button on code and run sendCode"""
        if btnname in self.data:
            return self.data[btnname]['On']

    def buttonOff(self, btnname):
        """buttonOff: get button off code and run sendCode"""
        if btnname in self.data:
            return self.data[btnname]['Off']


class IR(JsonConfig):
    """Class IR: Sendign IR codes"""

    def button(self, device, btnName):
        """button: return button code,mode,bits. device-device name e.g. tv ,btnName - name of button e.g. power, >> """
        if device in self.data:
            if btnName in self.data[device]['buttons']:
                return self.data[device]['buttons'][btnName], self.data[device]['mode'], self.data[device]['bits']


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


class Commands(JsonConfig):
    """Class Commands"""

    def runCmd(self, cmd, state):
        """runCmd"""
        if cmd in self.data:
            if state in self.data[cmd]:
                return os.system(self.data[cmd][state])


class TcpServer(Thread):
    """docstring for TcpServer"""
    def __init__(self, queue, host='127.0.0.1', port='9999', bufsize='1024'):
        Thread.__init__(self)
        self.queue = queue

        if host == 'auto':
            self.host = socket.gethostbyname(socket.gethostname())
        else:
            self.host = host

        self.port = int(port)
        self.bufsize = int(bufsize)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.loop = True
        self.conn = None
    
    def run(self):
        """docstring for serve_forever"""
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        while self.loop:
            print('tcp ready')
            self.conn, addr = self.sock.accept()
            print('Connected by', addr)
            data = self.conn.recv(self.bufsize)
            if not data:
                self.conn.close()
                continue
            data = data.decode()
            data = data.rstrip()
            self.queue.put(data)
            # self.conn.sendall(self.getAnswer())
            # print('ans : {0}'.format(self.getAnswer()))
            self.conn.close()

    def close(self):
        """docstring for close"""
        self.loop = False
        #self.sock.shutdown(1)
        self.sock.close()
        

class SerialServer(Thread):
    """docstring for SerialServer"""
    def __init__(self, queue,serialPort,brate=9600):
        Thread.__init__(self)
        self.queue = queue
        self.serialPort = serialPort
        self.baudrate = brate
        self.controller = None
        self.loop = True
        
    
    def __connect(self):
        """docstring for __reconnect"""
        while True:
            if os.path.exists(self.serialPort):
                self.controller = serial.Serial(port=self.serialPort, baudrate=9600)
                break
            sleep(3)
                
    def readSerial(self):
        """docstring for openSerial"""
         
        while self.loop:
            try:
                if self.controller.readable():
                    print('serial ready')
                    data = self.controller.readline()
                    data = data.decode()
                    data = data.rstrip()
                    self.queue.put(data)
            except:
                self.__connect()
                
    
    def writeSerial(self,data):
        """docstring for writeSerial"""
        if self.controller.writable():
            data = '{0}\n'.format(data)
            self.controller.write(bytearray(data,'ascii'))
        
    def run(self):
        """docstring for run"""
        self.__connect()
        self.readSerial()
        
    def close(self):
        """docstring for close"""
        self.loop = False


class SmartHome:
    """docstring for SmartHome"""
    def __init__(self, configFile):
        self.config = Config()
        self.config.loadFromFile(configFile)
        self.queue = Queue()
        self.loop = True
        self.tcpSrv = TcpServer(self.queue, self.config['host'], self.config['port'])
        self.serialSrv = SerialServer(self.queue, self.config['serial'])
        self.scenes = Scenes(self.config['scenedir'])
        self.rf = RF433()
        self.ir = IR()
        self.color = Colors()
        self.command = Commands()

    def __setup(self):
        """__setup"""
        self.scenes.loadScenes()
        self.rf.loadConfig(self.config['rf_config'])
        self.ir.loadConfig(self.config['ir_config'])
        self.color.loadConfig(self.config['colors_config'])
        self.command.loadConfig(self.config['commands_config'])

        self.tcpSrv.daemon = True
        self.tcpSrv.start()
        self.serialSrv.daemon = True
        self.serialSrv.start()

    def debug(self, msg):
        if self.config['debug'] == "False": return
        #colors
        green="\x1b[;32m"
        yellow="\x1b[;33m"
        default="\x1b[;00m"
        # end colors
        sys.stderr.write('{0}>>> {1}DEBUG: {2}{3}\n'.format(green,yellow,default,msg))

    def setRGB(self, s, fade=True):
        """setRGB"""
        r, g, b = s.split('.')
        if fade:
            self.serialSrv.writeSerial('F.{0}.{1}.{2}'.format(r, g, b))
        else:
            self.serialSrv.writeSerial('C.{0}.{1}.{2}'.format(r, g, b))

    def sendIR(self, code, mode, bits):
        """sendIR"""
        self.serialSrv.writeSerial('I.{0}.{1}.{2}'.format(code, mode, bits))

    def sendRF(self,s):
        """docstring for sendRF"""
        self.serialSrv.writeSerial('W.{0}'.format(code))

    def getTemp(self, s):
        """docstring for getTemp"""

        self.serialSrv.writeSerial('T.{0}'.format(s))
        sleep(0.2)
        ret = self.queue.pop()
        self.debug('temp : {0}'.format(ret))
        self.setAnswer(ret)
        return ret
        
    def getLight(self, s):
        """docstring for getTemp"""

        self.serialSrv.writeSerial('L.{0}'.format(s))
        sleep(0.2)
        ret = self.queue.pop()
        self.debug('temp : {0}'.format(ret))
        self.setAnswer(ret)
        return ret    
        
    def runScene(self, sc):
        """docstring for runScene"""
        self.debug(sc)
    
    def runCmd(self, s):
        """docstring for runCmd"""
        self.debug(s)
    
    def parseEvent(self, s):
        """docstring for parseEvent"""
        
        self.debug(s)
        self.setAnswer('')
        s = s.strip()
        args = s.split('.',2)
        if len(args) == 3:
            pcmd = args[0]
            cmd = args[1]
            arg = args[2]
        else:
            return
        
        if pcmd == 'set':
            if cmd == 'exit':
                self.stop()
            elif cmd == 'cmd':
                self.runCmd(arg)
            elif cmd == 'rgb':
                self.setRGB(arg)
            elif cmd == 'scene':
                self.runScene(arg)
            elif cmd == 'rf':
                self.sendRF(arg)
            
        elif pcmd == 'get':
            if cmd == 'light':
                self.getLight(arg)
            elif cmd == 'temp':
                self.getTemp(arg)

    def exit(self, status=0):
        """docstring for exit"""
        self.debug('exit status = {0}'.format(status))
        sys.exit(status)
    
    def start(self):
        """main loop"""
        self.__setup()

        while self.loop:
            if self.queue.notEmpty():
                self.parseEvent(self.queue.pop())
            else:
                sleep(1)
                
    def stop(self,*args):
        """stop mainloop"""
        self.tcpSrv.close()
        self.serialSrv.close()
        self.loop = False
        self.exit()
            
#########################################################################################
        
def usage():
    print('{0} version : {1}'.format(os.path.basename(sys.argv[0]),__version__))
    print('usage : {0} [start|stop|restart]'.format(os.path.basename(sys.argv[0])))


def print_help():
    print('-h --help     : print help screen')
    print('-c --config   : path to config file')
    sys.exit(0)


def stop_app(configFile):
    """docstring for stop_app"""
    config = Config()
    config.loadFromFile(configFile)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((config['host'], int(config['port'])))
        sock.sendall('set.cmd.exit\n'.encode())

        # Receive data from the server and shut down
        received = sock.recv(1024)
        sock.close()
    except:
        sys.stderr.write('SmartHome is not running\n')
    finally:
        sock.close()
    

if __name__ == "__main__":
  
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'hc:', ['help', 'config:'])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(1)
    #change assert to somting better :) 
    configFile = '/etc/SmartHome/SmartHome.conf'
    for o,a in opts:
        if o in ('-h', '--help'):
            print_help()
        elif o in ('-c', '--config'):
            configFile = a
        else:
            assert False, "unhandled option"
    
    if args == []:
        usage()
        sys.exit(1)

    srv = SmartHome(configFile)
    signal.signal(signal.SIGINT, srv.stop)
    signal.signal(signal.SIGHUP, srv.stop)
    signal.signal(signal.SIGQUIT, srv.stop)
    signal.signal(signal.SIGTERM, srv.stop)
    
    for a in args:
        if a == "start":
            srv.start()
        elif a == "stop":
            stop_app(configFile)
        else:
            assert False, "unhandled option"