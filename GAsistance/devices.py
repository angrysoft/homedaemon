class Devices:
    id = None
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

