import json
# https://developers.google.com/actions/reference/smarthome/errors-exceptions


class Actions:
    def __init__(self, data):
        try:
            self.req = json.loads(data)
        except json.JSONDecodeError as err:
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


class Intent:
    def __init__(self, requestId, _payload):
        self.requestId = requestId
        print(self.__class__.__name__)
        for i in _payload:
            print(type(_payload[i]), i)


class Sync:
    def __init__(self, requestId):
        self.requestId = requestId

    def response(self):
        _response = dict()
        _response['payload'] = dict()
        _response['payload']['devices'] = self._get_devices()
        _response['requestId'] = self.requestId
        return _response

    def _get_devices(self):
        all_devices = list()
        return all_devices


class Query(Intent):

    def response(self):
        return {}


class Execute(Intent):

    def response(self):
        return {}


class Disconnect:

    @staticmethod
    def response():
        return {}

