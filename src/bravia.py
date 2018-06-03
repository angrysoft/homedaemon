import urllib.parse
import urllib.request
import json
import socket
import struct


def wake_on_lan(macaddress):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = ''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('', 7))

class Bravia:
    """Navigate to: [Settings] → [Network] → [Home Network Setup] → [IP Control]
        Set [Authentication] to [Normal and Pre-Shared Key]
        There should be a new menu entry [Pre-Shared Key]. Set it for example to 0000.
    """

    def __init__(self, ip, psk='0000'):
        self.host = 'http://{}'.format(ip)
        self.psk = psk
        self.commands = {}

    def isOn(self):
        ret = json.loads(self._send('/sony/system', data=self._jsonCmd("getPowerStatus")))
        # try:
        #     if ret.has_key('result'):
        #         if data['result'][0]['status'] == "standby":
        #             # TV is in standby mode, and so not on.
        #             return False
        #         elif data['result'][0]['status'] == "active":
        #             # TV really is on
        #             return True
        #         else:
        #             # Assume it's not on.
        #             print
        #             "Uncaught result"
        #             return False
        #     if data.has_key('error'):
        #         if 404 in data['error']:
        #             # TV is probably booting at this point - so not available yet
        #             return False
        #         elif 403 in data['error']:
        #             # A 403 Forbidden is acceptable here, because it means the TV is responding to requests
        #             return True
        #         else:
        #             print
        #             "Uncaught error"
        #             return False
        #     return True
        # except requests.exceptions.ConnectTimeout:
        #     print
        #     "No response, TV is probably off"
        #     return False
        # except requests.exceptions.ConnectionError:
        #     print
        #     "TV is certainly off."
        #     return False
        # except requests.exceptions.ReadTimeout:
        #     print
        #     "TV is on but not accepting commands yet"
        #     return False
        # except ValueError:
        #     print
        #     "Didn't get back JSON as expected"
        #     # This might lead to false negatives - need to check
        #     return False

    def getAllCommands(self):
        ret = self._send('sony/system', data=self._jsonCmd('getRemoteControllerInfo'))
        #return json.dumps(ret, indent=4, ensure_ascii=False)
        ret = json.loads(ret)
        ret = ret.get('result')[1]
        if type(ret) == list:
            for func in ret:
                print(func)

    def sendCommand(self, cmd):
        if not self.commands:
            self.commands = self.getAllCommands()

        if cmd in self.commands:
            header = {'SOAPACTION': 'urn:schemas-sony-com:service:IRCC:1#X_SendIRCC',
                      'X-Auth-PSK': self.psk}
            data = '''
                        <?xml version="1.0"?>
                            <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                                <s:Body>
                                    <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
                                        <IRCCCode>{}</IRCCCode>
                                    </u:X_SendIRCC>
                                </s:Body>
                            </s:Envelope>'''.format(cmd)
            return self._send('sony/IRCC', header=header, data=data)

    def _jsonCmd(self, cmd, params=[], pId=10, version='1.0'):
        return json.dumps({'method': cmd,
                           'params': params,
                           'id': pId,
                           'version': version})

    def _send(self, url, header={}, data=None):
        _url = '{}/{}'.format(self.host, url)
        req = urllib.request.Request(_url, headers=header, method='POST', data=data.encode())

        with urllib.request.urlopen(req) as response:
            data = response.read()
            data = data.decode()
            return data
