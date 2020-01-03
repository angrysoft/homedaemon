#!/usr/bin/python
import json
from gasistant import get_devices_list
from pprint import pprint

a_exec = '''{
  "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
  "inputs": [{
    "intent": "action.devices.EXECUTE",
    "payload": {
      "commands": [{
        "devices": [{
          "id": "158d000283b219.1",
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
a_exec_sc = '''{
  "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
  "inputs": [{
    "intent": "action.devices.EXECUTE",
    "payload": {
      "commands": [{
        "devices": [{
          "id": "Movie",
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
          "command": "action.devices.commands.ActivateScene",
          "params": {
            "deactivate": true
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
        "id": "0x0000000007e7bae0",
        "customData": {
          "fooValue": 74,
          "barValue": true,
          "bazValue": "foo"
        }
      },{
        "id": "158d00024e2e5b.1",
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

from gasistant import Actions

gs = Actions(a_exec_sc)
print(gs.execute())
pprint(gs.response)
