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
from oauth import OAuth
from devices import Actions
# import websockets

app = Flask(__name__)

logging.basicConfig(filename='gast.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logging.warning('app starts')


@app.route('/', methods=['GET', 'POST'])
def index():
    """rfSend"""
    if request.method == 'GET':
        logging.warning('index get {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        return request.args.get('status', 'ooops something is wrong')
    elif request.method == 'POST':
        logging.warning('index post {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        status = 'ok'
    return redirect('/?status={}'.format(status))


@app.route('/auth')
def auth():
    """rfSend"""
    if request.method == 'GET':
        logging.warning('auth get {}, {}'.format(request.args,
                                                         request.headers))
        url = '/auth'
        if request.args.get('response_type', '') == 'code':
            g_auth = OAuth()
            url = g_auth.auth(request.args)
            logging.warning(url)
        return render_template('auth.html', uri=url)


@app.route('/auth/token', methods=['POST'])
def token():
    """rfSend"""
    logging.warning('token post {}, {}'.format(request.form,
                                                       request.headers))
    g_auth = OAuth()
    status = 400
    data = '{"error": "invalid_grant"}'
    if request.form.get('grant_type') == 'authorization_code':
        status, data = g_auth.get_new_token(request.form)
    elif request.form.get('grant_type') == 'refresh_token':
        status, data = g_auth.refresh_token(request.form)
    elif request.form.get('grant_type') == 'urn:ietf:params:oauth:grant-type:jwt-bearer':
        pass

    logging.warning(f'token: {status}, {data}')

    return app.response_class(response=data,
                              status=status,
                              mimetype='application/json')


@app.route('/status', methods=['GET', 'POST'])
def status():
    """rfSend"""
    g_auth = OAuth()
    _response = ''
    _status = 200
    if request.method == 'GET':
        logging.warning('status get {}, {}, {}, {}'.format(request.args,
                                                          request.form,
                                                          request.data,
                                                          request.headers))
        return request.args.get('status', 'ooops something is wrong')

    elif request.method == 'POST':
        logging.warning('status post {}, {}'.format(request.data, request.headers.get('Authorization')))

        if g_auth.log_by_token(request.headers.get('Authorization', '')):
            g_action = Actions(request.data)
            _response = g_action.response
        else:
            _response = '{"error":"user_not_found"}'
            _status = 401

        return app.response_class(response=_response,
                                  status=_status,
                                  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False) #, port=80)
    # 
