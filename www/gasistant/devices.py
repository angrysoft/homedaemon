#!/usr/bin/python3
import json
import pprint

a_exec = '''{
  "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
  "inputs": [{
    "intent": "action.devices.EXECUTE",
    "payload": {
      "commands": [{
        "devices": [{
          "id": "123",
          "customData": {
            "fooValue": 74,
            "barValue": true,
            "bazValue": "sheepdip"
          }
        },{
          "id": "456",
          "customData": {
            "fooValue": 36,
            "barValue": false,
            "bazValue": "moarsheep"
          }
        }],
        "execution": [{
          "command": "action.devices.commands.OnOff",
          "params": {
            "on": true
          }
        }]
      }]
    }
  }]
}
'''
a_query = '''
{
  "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
  "inputs": [{
    "intent": "action.devices.QUERY",
    "payload": {
      "devices": [{
        "id": "123",
        "customData": {
          "fooValue": 74,
          "barValue": true,
          "bazValue": "foo"
        }
      },{
        "id": "456",
        "customData": {
          "fooValue": 12,
          "barValue": false,
          "bazValue": "bar"
        }
      }]
    }
  }]
}
'''

a_sync = '''{
  "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
  "inputs": [{
    "intent": "action.devices.SYNC"
  }]
}'''


class Actions:
    class _Sub:
        pass

    def __init__(self, data):
        try:
            self.req = json.loads(data)
        except json.JSONDecodeError as err:
            return err

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
                self.payload= i.get('payload', {})

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


# gex = Actions(a_exec)
# gq = Actions(a_query)
gs = Actions(a_sync)
print(gs.response)


class Devices:
    def __init__(self):
        self.id = -1
        self.type = ''
        self.traits = list()
        self.name = {
            'defaultNames': [],
            'name': '',
            'nicknames': []
        }
        self.willReportState = False
        self.roomHint = ''
        self.deviceInfo = {
            'manufacturer': '',
            'model': '',
            'hwVersion': '',
            'swVersion': ''
        }
        self.customData = {}
        self.attributes = {}


class Outlet(Devices):
    def __init__(self):
        super(Outlet, self).__init__()
        self.type = 'action.devices.types.OUTLET'
        self.traits.append('action.devices.traits.OnOff')


class Light(Devices):
    def __init__(self):
        super(Light, self).__init__()
        self.type = 'action.devices.types.LIGHT'


d = Devices()
print(d.__dict__)