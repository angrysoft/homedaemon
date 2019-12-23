import jwt
import json
import socket
import ssl
from io import BytesIO
import time

class TcpRead:
    def __init__(self, ip, port, secret):
        self.ip = ip
        self.port = port
        self.secret = secret
    
    def reader(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        with socket.create_connection((self.ip, self.port)) as sock:
            with context.wrap_socket(sock, server_hostname='ferdek.angrysoft.ovh') as ssock:
                encoded = jwt.encode({'api':'1.0', 'client': 'www'}, self.secret, algorithm='HS256')
                ssock.send(encoded + '\n'.encode())
        
                with BytesIO() as buffer:
                    while True:
                        try:
                            resp = ssock.recv(1024)       # Read in some number of bytes -- balance this
                        except BlockingIOError:
                            print("sleeping")           # Do whatever you want here, this just
                            # time.sleep(2)               #   illustrates that it's nonblocking
                        else:
                            buffer.write(resp)          # Write to the BytesIO object
                            buffer.seek(0)              # Set the file pointer to the SoF
                            start_index = 0             # Count the number of characters processed
                            for line in buffer:
                                start_index += len(line)
                                line = line.decode()
                                yield line.strip()       # Do something with your line

                            """ If we received any newline-terminated lines, this will be nonzero.
                                In that case, we read the remaining bytes into memory, truncate
                                the BytesIO object, reset the file pointer and re-write the
                                remaining bytes back into it.  This will advance the file pointer
                                appropriately.  If start_index is zero, the buffer doesn't contain
                                any newline-terminated lines, so we set the file pointer to the
                                end of the file to not overwrite bytes.
                            """
                    
                            if start_index:
                                buffer.seek(start_index)
                                remaining = buffer.read()
                                buffer.truncate(0)
                                buffer.seek(0)
                                buffer.write(remaining)
                            else:
                                buffer.seek(0, 2)
    
    def writer(self, msg):
        context = ssl.create_default_context()
        context.check_hostname = False
        with socket.create_connection((self.ip, self.port)) as sock:
            with context.wrap_socket(sock, server_hostname='ferdek.angrysoft.ovh') as ssock:
                encoded = jwt.encode({'api':'1.0', 'client': 'www'}, self.secret, algorithm='HS256')
                ssock.send(encoded + '\n'.encode())
                ssock.send(msg + '\n'.encode())
                ssock.close()
