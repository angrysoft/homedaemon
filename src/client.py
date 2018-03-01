#!/usr/bin/env python

# -*- coding: utf-8 -*-
import socket
import os

print("Connecting...")
sock = '/tmp/housed.sock'
if os.path.exists(sock):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.connect(sock)
    print("Ready.")
    x = 'quit'
    client.send(x.encode('utf-8'))
    client.close()
else:
    print("Couldn't Connect!")
    print("Done")