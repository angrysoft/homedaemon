import json
from .devices import get_devices_list, QueryDevice
# https://developers.google.com/actions/reference/smarthome/errors-exceptions


class Actions:
    def __init__(self, data):
        try:
            self.req = json.loads(data)
        except json.JSONDecodeError:
            return

        self.requestId = self.req.get('requestId')
        self.intent = ''
        self.payload = {}
        self._get_inputs()
        self._response = {'requestId': self.requestId,
                          'payload': {
                              'errorCode': 'notSupported'
                          }}
        self._action()

    def _get_inputs(self):
        for i in self.req.get('inputs', []):
            if type(i) == dict:
                self.intent = i.get('intent', '')
                self.payload = i.get('payload', {})

    def _action(self):
        _intent = None
        if self.intent == 'action.devices.SYNC':
            _intent = Sync(self.requestId)
        elif self.intent == 'action.devices.QUERY':
            _intent = Query(self.requestId, self.payload)
        elif self.intent == 'action.devices.EXECUTE':
            _intent = Execute(self.requestId, self.payload)
        elif self.intent == 'action.devices.DISCONNECT':
            _intent = Disconnect()

        if _intent:
            self._response = _intent.response()

    @property
    def response(self):
        return json.dumps(self._response)


class Sync:
    def __init__(self, requestId):
        self.requestId = requestId

    def response(self):
        _response = dict()
        _response['requestId'] = self.requestId
        _response['payload'] = dict()
        _response['payload']['agentUserId'] = '2ed39'
        _response['payload']['devices'] = self._get_devices()
        return _response

    def _get_devices(self):
        return get_devices_list()


class Query:
    def __init__(self, requestId, payload):
        self.requestId = requestId
        self.payload = payload
    
    def _get_devices_status(self):
        ret = dict()
        try: 
            for dev in self.payload['devices']:
                q = QueryDevice(dev)
                ret[dev['id']] = q.query()
        except Exception:
            return {}
        return ret
        
    def response(self):
        _response = dict()
        _response['requestId'] = self.requestId
        _response['payload'] = dict()
        _response['payload']['agentUserId'] = '2ed39'
        _response['payload']['devices'] = self._get_devices_status()
        return _response


class Execute:

    def response(self):
        return {}


class Disconnect:

    @staticmethod
    def response():
        return {}

