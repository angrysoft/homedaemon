import socket
import json
import binascii
from Crypto.Cipher import AES


class Gateway:
    def __init__(self, ip='auto', sid='', gwpasswd=''):
        self.aes_key_iv = bytes([0x17, 0x99, 0x6d, 0x09, 0x3d, 0x28, 0xdd, 0xb3, 0xba, 0x69, 0x5a, 0x2e, 0x6f, 0x58, 0x56, 0x2e])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.multicast = ('224.0.0.50', 4321)
        if ip == 'auto':
            gateway = self.whois()
            self.unicast = (gateway.get('ip'), int(gateway.get('port')))
            self.sid = gateway.get('sid')
        else:
            self.unicast = (ip, 9898)
            self.sid = sid
        self.gwpassword = gwpasswd

    def whois(self):
        """Discover the gateway device multicast (IP: 224.0.0.50 peer_port: 4321 protocal: UDP)"""

        return self._send_multicast(cmd='whois')

    def get_device_list(self):
        """The command is sent via unicast to the UDP 9898 port of the gateway,
        which is used to obtain the sub-devices in the gateway."""

        return self._send_unicast(cmd='discovery')

    def get_id_list(self):
        return self._send_unicast(cmd='get_id_list')

    def read_device(self, sid):
        """Reading devices
        Send the "read" command via unicast to the gateway's UDP 9898 port.
        Users can take the initiative to read the attribute status of each device,
        and the gateway returns all the attribute information associated with the device."""

        return self._send_unicast(cmd='read', sid=sid)

    def write_device(self, _model, _sid, _params):
        """Send the "write" command via unicast to the gateway's UDP 9898 port.
        When users need to control the device, the user can use the "write" command."""
        return self._send_unicast(cmd='write', model=_model, sid=_sid, params=_params, key=self.get_key())

    def read_all_devices(self):
        id_list = self.get_id_list()
        id_list = json.loads(id_list.get('data'))
        ret = []
        for _id in id_list:
            ret.append(self.read_device(_id))
        return ret

    def _cmd(self, args):
        print(args)
        return json.dumps(args)

    def _answer(self):
        data_bytes, addr = self.sock.recvfrom(1024)
        if data_bytes:
            return json.loads(data_bytes.decode())
        else:
            return ''

    def _send_multicast(self, **kwargs):
        self.sock.sendto(self._cmd(kwargs).encode(), self.multicast)
        return self._answer()

    def _send_unicast(self, **kwargs):
        self.sock.sendto(self._cmd(kwargs).encode(), self.unicast)
        return self._answer()

    def get_token(self):
        return self.read_device(self.sid)

    def get_key(self, gwpass):
        """Get current gateway key"""
        cipher = AES.new(gwpass, AES.MODE_CBC, self.aes_key_iv)
        encrypted = cipher.encrypt(self.get_token())
        return binascii.hexlify(encrypted)

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    gw = Gateway(gwpasswd='cjvt7wr3q7df72rq')
    print(gw.whois())
    # print(gw.get_id_list())
    print(gw.get_device_list())
    # print(gw.read_all_devices())
    print(gw.get_token())
