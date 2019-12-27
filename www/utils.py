import jwt
import json
import socket
import ssl


class TcpWrite:
    def __init__(self, ip, port, secret):
        self.ip = ip
        self.port = port
        self.secret = secret
    
    def writer(self, msg):
        context = ssl.create_default_context()
        context.check_hostname = False
        with socket.create_connection((self.ip, self.port)) as sock:
            with context.wrap_socket(sock, server_hostname='ferdek.angrysoft.ovh') as ssock:
                encoded = jwt.encode({'api':'1.0', 'client': 'www'}, self.secret, algorithm='HS256')
                ssock.sendall(encoded + '\n'.encode())
                ssock.sendall(msg + '\n'.encode())
                ssock.shutdown()
                ssock.close()
            sock.shutdown()
            sock.close()
