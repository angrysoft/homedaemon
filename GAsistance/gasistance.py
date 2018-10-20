#!/usr/bin/env python3
# gasistance.py
# Copyright (C) 2018  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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
__version__ = '0.1'

import logging
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
# import websockets
import os
import json
import sqlite3
import jwt

app = Flask(__name__)

client_id = '386751861706-082sa86m5ak3vtp3999eabd6e4eijjgu.apps.googleusercontent.com'
secret = 'WW_AKiWaz35Sc4IFAGT69eH9'
logging.basicConfig(filename='gast.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('app starts')

#
@app.route('/', methods=['GET', 'POST'])
def index():
    """rfSend"""
    if request.method == 'GET':
        logging.warning('request get {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        logging.warning('request post {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        status = 'ok'
        # print(jwt.decode(data, secret, algorithms=['HS256']))
    return redirect('/?status={}'.format(status))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)