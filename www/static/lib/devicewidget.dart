import 'dart:html';
import 'dart:convert';

import 'dart:mirrors';

class Devices {
  Map<String,BaseDeviceWidget> _devices;

  Devices() {
    this._devices = new Map();
  }

  void register( Map<String,dynamic> devData, Function evSend) {
    print('Registring: ${devData["model"]}');
    switch(devData['model']) {
      case 'ctrl_neutral1':
      {
        this._devices[devData['sid']] = new CtrlNeutral1(devData, evSend);
      }
      break;
      case 'ctrl_neutral2':
      {
        this._devices[devData['sid']] = new CtrlNeutral2(devData, evSend);
      }
      break;
      case 'plug':
      {
        this._devices[devData['sid']] = new Plug(devData, evSend);
      }
      break;
      case 'bslamp1':
      {
        this._devices[devData['sid']] = new Bslamp1(devData, evSend);
      }
      break;
      case 'color':
      {
        this._devices[devData['sid']] = new Color(devData, evSend);
      }
      break;
      case 'rgbstrip':
      {
        this._devices[devData['sid']] = new RgbStrip(devData, evSend);
      }
      break;
      case 'sensor_ht':
      {
        this._devices[devData['sid']] = new SensorHt(devData);
      }
      break;
      case 'weather.v1':
      {
        this._devices[devData['sid']] = new WeatherV1(devData);
      }
      break;
      case 'magnet':
      {
        this._devices[devData['sid']] = new Magnet(devData);
      }
      break;
      case 'bravia':
      {
        this._devices[devData['sid']] = new Bravia(devData, evSend);
      }
      break;
    }
  }

  void refresh(String data) {
    try {
      Map<String, dynamic> info = json.decode(data);
      if (this._devices.containsKey(info['sid']) && info.containsKey('data')) {
        this._devices[info['sid']].refreshStatus(info['data']);
      }
    } catch (e) {
      print('error:$e ${data}');
    }
  }
}


class CtrlNeutral2 extends CtrlNeutral1 {
  Button channel_1;

  CtrlNeutral2(Map<String,dynamic> devData, Function evSend) : super(devData, evSend) {
    this.channel_1 = new Button('channel_1', this.sid);
    this.channel_1.setStatus(this.devData['channel_1']);
    this.channel_1.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    super.refreshStatus(devData);
    this.channel_1.setStatus(devData['channel_1']);
  }
}


class CtrlNeutral1 extends DeviceWidget {
  Button channel_0;

  CtrlNeutral1(Map<String,dynamic> devData, Function evSend) : super (devData, evSend) {
    this.channel_0 = new Button('channel_0', this.sid);
    this.channel_0.setStatus(this.devData['channel_0']);
    this.channel_0.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    this.channel_0.setStatus(devData['channel_0']);
  }
}


class Plug extends DeviceWidget {
  Button power;

  Plug(Map<String,dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('status', this.sid);
    this.power.setStatus(this.devData['status']);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
  }

  @override
  void refreshStatus(Map<String,dynamic> devData) {
    this.power.setStatus(devData['status']);
  }
}


class RgbStrip extends DeviceWidget {
  Button power;
  SetButton setBtn;
  
  RgbStrip(Map<String,dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('status', this.sid);
    this.power.setStatus(this.devData['status']);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    this.setBtn = new SetButton(this.sid);
  }
}


class Color extends Bslamp1 {
  Color(Map<String,dynamic> devData, Function evSend) : super(devData, evSend);
}

class Bravia extends Bslamp1 {
  Bravia(Map<String,dynamic> devData, Function evSend) : super(devData, evSend);
}

class Bslamp1 extends DeviceWidget {
  Button power;
  SetButton setBtn;

  Bslamp1(Map<String,dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('power', this.sid);
    this.power.setStatus(this.devData['power']);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    this.setBtn = new SetButton(this.sid);
  }
}


class DeviceWidget implements BaseDeviceWidget {
  Map<String,dynamic> devData;
  Function evSend;

  DeviceWidget(Map<String,dynamic> devData, Function evSend) {
    this.devData = devData;
    this.evSend = evSend;
  }

  String get sid {return this.devData['sid'];}

  void set sid(String _sid) {
    this.devData['sid'] = _sid;
  }

  String get model {return this.devData['model'];}
  void set model(String _model) {
    this.devData['model'] = _model;
  }

  void refreshStatus(Map<String,dynamic> devData) {
    print('${this.devData['sid']} $devData');
  }

  void send(ButtonElement btn) {
    Map<String, dynamic> msg = new Map();
    String cmdname = '';
    if (btn.dataset.containsKey('cmd')) {
      cmdname = btn.dataset['cmd'];
    } else {
      cmdname = btn.dataset['status'];
    }
    msg['cmd'] = 'write';
    msg['sid'] = this.sid;
    msg['data'] = {cmdname: btn.value};
    String data = json.encode(msg);
    HttpRequest.request('/dev/write', method: 'POST', sendData: data);
    print(data);
  }

}

class Magnet extends ReadOnlyDevice {
  Label status;
  Label vol;
  Magnet(Map<String,dynamic> devData) : super(devData) {
    this.status = new Label('status', this.sid);
    this.vol = new Label('voltage', this.sid);
    this.refreshStatus(devData);
  }

  @override
  void refreshStatus(Map<String,dynamic> devData) {
    this.status.setStatus(devData['status']);
    this.vol.setStatus((devData['voltage']).toString());
  }
}

class WeatherV1 extends SensorHt {
  Label pressure;

  WeatherV1(Map<String,dynamic> devData) : super(devData) {
    this.pressure = new Label('pressure', this.sid);
  }

  @override
  void refreshStatus(Map<String,dynamic> devData) {
    super.refreshStatus(devData);
    this.pressure.setStatus((int.parse(devData['pressure'])/100).floor().toString());
  }
}

class SensorHt extends ReadOnlyDevice {
  Label temp;
  Label humidity;
  Label vol;

  SensorHt(Map<String,dynamic> devData) : super(devData) {
    this.temp = new Label('temperature', this.sid);
    this.humidity = new Label('humidity', this.sid);
    this.vol = new Label('voltage', this.sid);
  }

  @override
  void refreshStatus(Map<String,dynamic> devData) {
    this.temp.setStatus((int.parse(devData['temperature'])/100).toString());
    this.humidity.setStatus((int.parse(devData['humidity'])/100).floor().toString());
    this.vol.setStatus((devData['voltage']).toString());
  }
}

class ReadOnlyDevice implements BaseDeviceWidget {
  Map<String,dynamic> devData;
  ReadOnlyDevice(Map<String,dynamic> devData) {
    this.devData = devData;
  }

  String get sid {return this.devData['sid'];}

  void set sid(String _sid) {
    this.devData['sid'] = _sid;
  }

  String get model {return this.devData['model'];}
  void set model(String _model) {
    this.devData['model'] = _model;
  }

  void refreshStatus(Map<String,dynamic> devData) {
    print('${this.devData['sid']} $devData');
  }
}

abstract class BaseDeviceWidget {
  void refreshStatus(Map<String,dynamic> devData);
  String get sid;
  void set sid(String _sid);
  String get model;
  void set model(String _model);

}

class Button {
  String name;
  ButtonElement btn;
  bool _status = false;

  Button(String name, String sid) {
    this.name = name;
    this.btn = querySelector('button.${name}[data-sid="${sid}"]');
  }

  bool getStatus() {
    return this._status;
  }
  
  setStatus(String st) {
    if (st == 'on') {
      this._status = true;
      this.btn
        ..classes.add('orange')
        ..text = 'off'
        ..value = 'off';

    } else if (st == 'off') {
      this._status = false;
      this.btn
        ..classes.remove('orange')
        ..text = 'on'
        ..value = 'on';
    }
  }  
}

class SetButton {
  ButtonElement btn;

  SetButton(String sid) {
    this.btn = querySelector('button.color-set-button[data-sid="${sid}"]');
  }
}

class Label {
  String name;
  SpanElement info;

  Label(String name , String sid) {
    this.name = name;
    this.info = querySelector('span.${name}[data-sid="${sid}"]');
  }

  setStatus(String st) {
      this.info.text = st;
  } 
}