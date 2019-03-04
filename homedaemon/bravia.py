import urllib.parse
import urllib.request
import json
import socket
import struct


class Bravia:
    """Navigate to: [Settings] → [Network] → [Home Network Setup] → [IP Control]
        Set [Authentication] to [Normal and Pre-Shared Key]
        There should be a new menu entry [Pre-Shared Key]. Set it for example to 0000.
    """

    def __init__(self, ip, psk='0000', macaddres=None):
        self.host = 'http://{}'.format(ip)
        self.psk = psk
        self.commands = {}
        self._macaddr = ''
        self.macaddr = macaddres

    @property
    def macAddress(self):
        return self._macaddr

    @macAddress.setter
    def macAddress(self, val):
        if len(val) == 17:
            sep = val[2]
            val = val.replace(sep, '')
            self._macaddr = val
        elif len(val) == 12:
            self._macaddr = val
        else:
            raise ValueError('Incorrect MAC address format')

    def is_on(self):
        try:
            ret = json.loads(self._send('sony/system', data=self._jsonCmd("getPowerStatus"), timeout=2)) # , pId='1')))
        except socket.timeout:
            return False
        except:
            return False

        error = ret.get('error')
        if 'result' in ret:
            ret = ret.get('result')[0]
        if ret:
            status = ret.get('status')
            if status == 'standby':
                return False
            elif status == 'active':
                return True
            elif error:
                if error == 404:
                    # TV is probably booting at this point - so not available yet
                    return False
                elif error == 403:
                    # A 403 Forbidden is acceptable here, because it means the TV is responding to requests
                    return True
                else:
                    print("Uncaught error")
                    return False

    def get_all_commands(self):
        ret = json.loads(self._send('sony/system', data=self._json_cmd('getRemoteControllerInfo')))
        ret = ret.get('result')[1]
        commands = dict()
        if type(ret) == list:
            for func in ret:
                if 'name' in func:
                    commands[func.get('name')] = func.get('value')
        return commands

    def send_command(self, cmd):
        if not self.commands:
            self.commands = self.get_all_commands()
        if cmd in self.commands:
            header = {'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
                      'X-Auth-PSK': '{}'.format(self.psk),
                      'Content-Type': 'text/xml; charset=UTF-8'}

            data = "<?xml version=\"1.0\"?>" \
                 "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" \
                 "<s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\">" \
                 "<IRCCCode>{}</IRCCCode>" \
                 "</u:X_SendIRCC>" \
                 "</s:Body>" \
                 "</s:Envelope>".format(self.commands.get(cmd))
            return self._send('sony/IRCC', header=header, data=data)

    def _json_cmd(self, cmd, params=[], pId=10, version='1.0'):
        return json.dumps({'method': cmd,
                           'params': params,
                           'id': pId,
                           'version': version})

    def _send(self, url, header={}, data=None, timeout=10):
        _url = '{}/{}'.format(self.host, url)
        if data:
            data = data.encode()
        try:
            req = urllib.request.Request(_url, headers=header, method='POST', data=data)

            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                data = data.decode()
                return data
        except OSError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err)

    def power_on(self):
        # if self.isOn():
        if False:
            return 'Power is on'
        else:
            data = b'FFFFFFFFFFFF' + (self.macAddress * 20).encode()
            send_data = b''

            # Split up the hex values and pack.
            for i in range(0, len(data), 2):
                send_data += struct.pack('B', int(data[i: i + 2], 16))

            # Broadcast it to the LAN.
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(send_data, ('255.255.255.255', 7))

    def power_off(self):
        self.send_command('PowerOff')
