#!/usr/bin/python3

import os

if os.path.exists('files.txt'):
    with open('files.txt') as ff:
        for f in ff.readline():
            if os.path.exists(f):
                print('Remove {}'.format(f))
                os.unlink(f)
