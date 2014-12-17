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

#colors
black="\x1b[;30m"
red="\x1b[;31m"
green="\x1b[;32m"
yellow="\x1b[;33m"
blue="\x1b[;34m"
default="\x1b[;00m"
# end colors

#niby można użyć collections.deque 
class Queue:
    """docstring for Queue fifo list"""
    def __init__(self):
        self.l = []
        
    def put(self,arg):
        """docstring for put arg on end of list"""
        self.l.insert(0,arg)
    
    def pop(self):
        """docstring for pop"""
        return self.l.pop()
    
    def len(self):
        """docstring for len"""
        return len(self.l)


class Config(dict):
    
    def __init__(self):
        # default value
        self['debug']   = "False"
        self['host']    = 'localhost'
        self['port']    = '9999'
        self['bufsize'] = '1024'
        self['serial']  = '/dev/ttyUSB0'
        self['scenedir']= '/etc/SmartHome/Scenes'
        
    
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

class RF433:
    """Class RF433 send rf Code"""

    def __init__(self, rfCongFile):
        """Constructor for RF433"""
        self.rf = {}
        self.rfconf = rfCongFile

    def loadConfig(self):
        """loadConfig: load json config file"""
        with open(self.rfconf, 'r') as jdata:
            self.rf = json.load(jdata)

    def sendCode(self):
        """sendCode: send rf code to serial device"""
        pass

    def buttonOn(self, btnname):
        """buttonOn: get button on code and run sendCode"""
        if btnname in self.rf:
            self.sendCode(self.rf[btnname]['On'])

    def buttonOff(self, btnname):
        """buttonOff: get button off code and run sendCode"""
        if btnname in self.rf:
            self.sendCode(self.rf[btnname]['Off'])

class IR:
    """Class IR: Sendign IR codes"""

    def __init__(self, irConfFile):
        """Constructor for IR"""
        self.ir = {}
        self.ifconf = irConfFile

    def loadConfig(self):
        """loadConfig"""
        with open(self.irconf, 'r') as jdata:
            self.ir = json.load(jdata)



class TcpServer(Thread):
    """docstring for TcpServer"""
    def __init__(self, queue, answer, host='127.0.0.1', port='9999', bufsize='1024'):
        Thread.__init__(self)
        self.queue = queue
        self.getAnswer = answer

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
            sleep(1)
            self.conn.sendall(self.getAnswer())
            print('ans : {0}'.format(self.getAnswer()))
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
        self.queue = Queue()
        #
        self.config = Config()
        self.config.loadFromFile(configFile)
        self.loop = True
        self.answer = '\n'
        self.tcpSrv = TcpServer(self.queue, self.getAnswer, self.config['host'], self.config['port'])
        self.serialSrv = SerialServer(self.queue, self.config['serial'])
        self.sceneDir = self.config['scenedir']
        self.scenes = {}
        self.rf = RF433()
        self.ir = IR()
        
    def debug(self, msg):
        if self.config['debug'] == "False": return
        #colors
        green="\x1b[;32m"
        yellow="\x1b[;33m"
        default="\x1b[;00m"
        # end colors
        sys.stderr.write('{0}>>> {1}DEBUG: {2}{3}\n'.format(green,yellow,default,msg))

    def setAnswer(self, ans):
        """setAnswer"""
        self.answer = '{0}\n'.format(ans)

    def getAnswer(self):
        """getAnswer"""
        return self.answer.encode()

    def loadScenes(self):
        """loadScenes"""
        for s in os.listdir(self.config['scenedir']):
            if s.endswith('.sc'):
                self.debug('Load scene: {0}'.format(s))
                with (open('{0}/{1}'.format(self.config['scenedir'],s),'r')) as f:
                    self.scenes[s.rsplit('.',1)[0]] = f.read()

    def setRGB(self, s, fade=True):
        """setRGB"""
        r, g, b = s.split('.')
        if fade:
            self.serialSrv.writeSerial('F.{0}.{1}.{2}'.format(r,g,b))
        else:
            self.serialSrv.writeSerial('C.{0}.{1}.{2}'.format(r,g,b))
        self.setAnswer('OK')

    def sendIR(self):
        """sendIR"""
        # code.mode.bits
		# mode = SONY,NEC,OTHER,JVC
		# code = ir code
		# bits
        pass

    def sendRF(self,s):
        """docstring for sendRF"""
        self.serialSrv.writeSerial('W.{0}'.format(code))
        self.setAnswer('OK')
    
    def kodi(self, b):
        """docstring for startKodi"""
        if b:
            os.system('systemctl start kodi')
        else:
            os.system('systemctl stop kodi')
        self.setAnswer('OK')
    
    def transmission(self, b):
        """docstring for startTransmission"""
        if b:
            os.system('Transmission.sh start')
        else:
            os.system('Transmission.sh stop')
        self.setAnswer('OK')
        
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
        print(sc)
        if sc in self.scenes:
            exec(self.scenes[sc])
    
    def runCmd(self, s):
        """docstring for runCmd"""
        if s == 'exit':
            self.stop()
        elif s == 'startkodi':
            self.kodi(True)
        elif s == 'stopkodi':
            self.kodi(False)
        elif s == 'starttranssmision':
            self.transmission(True)
    
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
            if cmd == 'cmd':
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
        self.loadScenes()
        self.tcpSrv.daemon = True
        self.tcpSrv.start()
        self.serialSrv.daemon = True
        self.serialSrv.start()

        while self.loop:
            if self.queue.len() > 0:
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
            

        
    

