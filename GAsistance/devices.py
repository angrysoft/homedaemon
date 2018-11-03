import json
# https://developers.google.com/actions/reference/smarthome/errors-exceptions


class Devices:
    id = -1
    type = ''
    traits = list()
    name = {
        'defaultNames': [],
        'name': '',
        'nicknames': []
    }
    willReportState = False
    roomHint = ''
    deviceInfo = {
        'manufacturer': '',
        'model': '',
        'hwVersion': '',
        'swVersion': ''
    }
    customData = {}
    attributes = {}


class Outlet(Devices):
    pass


class Actions:
    pass



