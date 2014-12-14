import xbmc
import socket

class PlayerMonitor(xbmc.Player):
    """docstring for PlayerMonitor"""
    def __init__(self):
        super(PlayerMonitor, self).__init__()
        
    def sendEvent(self,ev):
        """docstring for sendEvent"""
        HOST, PORT = "192.168.0.102", 9999
        data = '{}\n'.format(ev)
        try:
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            pass

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data.encode())

            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()

        xbmc.log("PlayerMonitor Sent:     {0}".format(data))
        xbmc.log("PlayerMonitor Received: {0}".format(received.decode()))
    
    def onPlayBackStarted(self):
        """docstring for onPlayBackStarted"""
        self.sendEvent('')
        xbmc.log("Play")
    
    def onPlayBackResumed(self):
        """docstring for onPlayBackResumed"""
        xbmc.log('resumed')
    
    def onPlayBackPaused(self):
        """docstring for onPlayBackPaused"""
        xbmc.log("paused")
    
    def onPlayBackStopped(self):
        """docstring for onPlayBackStopped"""
        xbmc.log("Stop")
    
    def onPlayBackEnded(self):
        """docstring for onPlayBackEnded"""
        xbmc.log("end")
    
        
    
#run the program
xbmc.log("Service starting : PlayerMonitor")
pm = PlayerMonitor()
while(not xbmc.abortRequested):
    xbmc.sleep(100)
