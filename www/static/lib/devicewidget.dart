import 'dart:html';
import 'dart:convert';
import 'dart:async';
import 'modal.dart';

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

  Future refresh(String data) async {
    try {
      print(data);
      Map<String, dynamic> info = json.decode(data);
      if (this._devices.containsKey(info['sid']) && info.containsKey('data')) {
        await this._devices[info['sid']].refreshStatus(info['data']);
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
    if (devData.containsKey('channel_1')) {
      this.channel_1.setStatus(devData['channel_1']);
    }
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
    if (devData.containsKey('channel_0')) {
      this.channel_0.setStatus(devData['channel_0']);
    }
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
  void refreshStatus(Map<String, dynamic> devData) {
    if (devData.containsKey('status')) {
      this.power.setStatus(devData['status']);
    }
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

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    if (devData.containsKey('status')) {
      this.power.setStatus(devData['status']);
    }
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

  Bslamp1(Map<String, dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('power', this.sid);
    this.power.setStatus(this.devData['power']);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    this.setBtn = new SetButton(this.sid);
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    if (devData.containsKey('power')) {
      this.power.setStatus(devData['power']);
    }
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

  Future<void> send(ButtonElement btn) async {
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

    await HttpRequest.request('/dev/write', method: 'POST', sendData: data)
      .then((HttpRequest resp) {
      print('$data : ${resp.responseText}');
    }); 
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
    if (devData.containsKey('status')) {
      this.status.setStatus(devData['status']);
    }
    if (devData.containsKey('voltage')) {
      this.vol.setStatus((devData['voltage']).toString());
    }
  }
}

class WeatherV1 extends SensorHt {
  Label pressure;

  WeatherV1(Map<String,dynamic> devData) : super(devData) {
    this.pressure = new Label('pressure', this.sid);
    this.refreshStatus(devData);
  }

  void refreshStatus(Map<String,dynamic> devData) {
    print(this.pressure.runtimeType);
    super.refreshStatus(devData);
    if (devData.containsKey('pressure')) {
      this.pressure.setStatus((int.parse(devData['pressure'])/100).floor().toString());
    }
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
    this._refreshStatus(devData);
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    this._refreshStatus(devData);
  }

  void _refreshStatus(Map<String,dynamic> devData) {
    
    if (devData.containsKey('temperature')) {
      this.temp.setStatus((int.parse(devData['temperature'])/100).toString());
    }
    if (devData.containsKey('humidity')) {
      this.humidity.setStatus((int.parse(devData['humidity'])/100).floor().toString());
    }
    if (devData.containsKey('voltage')) {
      this.vol.setStatus((devData['voltage']).toString());
    }
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

class SetButton {
  ButtonElement btn;
  ColorSetterWindow colorWnd;
  SetButton(String sid) {
    this.colorWnd = new ColorSetterWindow(sid);
    this.btn = querySelector('button.color-set-button[data-sid="${sid}"]');
    this.btn.onClick.listen((ev) {
      this.colorWnd.showWindow();
    });
  }
}

class ColorSetterWindow {
  Modal colorWnd;
  Element back;
  String sid;
  ButtonElement btnRgb;
  ButtonElement btnCt;
  RangeInputElement bright = querySelector('#bright');
  RangeInputElement ct = querySelector('#ct');
  DivElement rgbTab;
  DivElement ctTab;
  InputElement color = querySelector('#color-picker');
  StreamSubscription eventBright;
  StreamSubscription eventCt;
  StreamSubscription eventColor;
  bool current = false;

  ColorSetterWindow(String sid) {
    this.sid = sid;
    this.rgbTab = querySelector('#rgb-tab');
    this.ctTab = querySelector('#ct-tab');
    this.btnCt = querySelector('#ct-btn');
    this.btnRgb = querySelector('#rgb-btn');
    this.colorWnd = new Modal.fromHtml('color-set');
    this.back = querySelector('#back');
    this.back.onClick.listen((e) {
      this.closeWindow();
    });
    this.btnCt.onClick.listen((event) {
      event.preventDefault();
      this.ctTab.classes.add('show');
      this.rgbTab.classes.remove('show');
    });

    this.btnRgb.onClick.listen((event) {
      event.preventDefault();
      this.rgbTab.classes.add('show');
      this.ctTab.classes.remove('show');
    });

    this.eventBright = this.bright.onChange.listen((e) {
      this.send('set_bright', this.bright.value);
    });

    this.eventCt = this.ct.onChange.listen((e) {
      this.send('set_ct_abx', this.ct.value);
    });

    this.eventColor = this.color.onChange.listen((e) {
      this.send('set_rgb', this.hexToRgb(this.color.value));
    });
  }
  
  showWindow() {
    this.setData();
    this.current = true;
    this.colorWnd.show();
  }

  closeWindow() {
    this.current = false;
    this.colorWnd.hide();
  }

  Future<void> send(String key, dynamic value) async {
    if (! this.current) {
      return;
    }
    Map<String, dynamic> msg = new Map();
    msg['cmd'] = 'write';
    msg['sid'] = this.sid;
    msg['data'] = {key: value};

    String data = json.encode(msg);
    await HttpRequest.request('/dev/write', method: 'POST', sendData: data)
      .then((HttpRequest resp) {
      print('$data : ${resp.responseText}');
    }); 
  }

  setData() {
    HttpRequest.getString('/dev/data/${this.sid}').then((String resp) {
        var data = jsonDecode(resp);
        if (data.containsKey('bright')) {
          this.bright.value = data['bright'].toString();
        }

        if (data.containsKey('ct')) {
          this.ct.value = data['ct'].toString();
        }

        if (data.containsKey('rgb')) {
          int rgbint;
          if (data['rgb'] is int) {
            rgbint = data['rgb'];
          } else {
            rgbint = int.parse(data['rgb']);
          }
          int b =  rgbint & 255;
          int g = (rgbint >> 8) & 255;
          int r =   (rgbint >> 16) & 255;
          print('${r}.${g}.${b}');
          this.color.value = this.rgbToHex(r, g, b);
        } else if (data.containsKey('red') && data.containsKey('green') && data.containsKey('blue')) {
          this.color.value = this.rgbToHex(data['red'], data['green'], data['blue']);
        }
    });
  }

  String rgbToHex(int r, int g, int b) {
    String hex = '#${r.toRadixString(16).padLeft(2,'0')}${g.toRadixString(16).padLeft(2,'0')}${b.toRadixString(16).padLeft(2,'0')}';
    print(hex);
    return hex;
  }

  Map<String,dynamic> hexToRgb(String h) {
    Map<String,dynamic> ret = new Map();

    if (h.length == 7) {
      int r = int.parse(h.substring(1,3),radix:16);
      int g = int.parse(h.substring(3,5),radix:16);
      int b = int.parse(h.substring(5,7),radix:16);
      ret = {'red': r, 'green': g, 'blue': b};
    }
    return ret;
  }
}


// class ColorSetter {
//   ColorSetterWindow wnd = new ColorSetterWindow();
//   String sid;
//   ButtonElement btnRgb;
//   ButtonElement btnCt;
//   DivElement rgbTab;
//   DivElement ctTab;
//   Map<String, dynamic> lampdata;
//   RangeInputElement bright = querySelector('#bright');
//   RangeInputElement ct = querySelector('#ct');
//   InputElement color = querySelector('#color-picker');
//   StreamSubscription eventBright;
//   StreamSubscription eventCt;
//   StreamSubscription eventColor;

//   ColorSetter(String sid) {
//     this.sid = sid;

//     this.btnCt = querySelector('#ct-btn');
//     this.btnRgb = querySelector('#rgb-btn');
//     this.rgbTab = querySelector('#rgb-tab');
//     this.ctTab = querySelector('#ct-tab');
//     this.btnCt.onClick.listen((event) {
//       event.preventDefault();
//       this.ctTab.classes.add('show');
//       this.rgbTab.classes.remove('show');
//     });

//     this.btnRgb.onClick.listen((event) {
//       event.preventDefault();
//       this.rgbTab.classes.add('show');
//       this.ctTab.classes.remove('show');
//     });
//   }

//   void refresh(Map<String,dynamic> data) {

//     if (data.containsKey('bright')) {
//       this.bright.value = data['bright'].toString();
//     }

//     if (data.containsKey('ct')) {
//       this.ct.value = data['ct'].toString();
//     }

//     if (data.containsKey('rgb')) {
//       int rgbint;
//       if (data['rgb'] is int) {
//         rgbint = data['rgb'];
//       } else {
//         rgbint = int.parse(data['rgb']);
//       }
//       int b =  rgbint & 255;
//       int g = (rgbint >> 8) & 255;
//       int r =   (rgbint >> 16) & 255;
//       print('${r}.${g}.${b}');
//       this.color.value = this.rgbToHex(r, g, b);
//     } else if (data.containsKey('red') && data.containsKey('green') && data.containsKey('blue')) {
//       this.color.value = this.rgbToHex(data['red'], data['green'], data['blue']);
//     }
//   }

//   void watchEvent() {
//     this.eventBright = this.bright.onChange.listen((e) {
//       this.sendBrightnes(this.bright.value);
//     });

//     this.eventCt = this.ct.onChange.listen((e) {
//       this.sendCt(this.ct.value);
//     });

//     this.eventColor = this.color.onChange.listen((e) {
//       this.sendRgb(this.hexToRgb(this.color.value));
//     });
//   }

//   void cancelWatchEvent() {
//     this.eventBright.cancel();
//     this.eventCt.cancel();
//     this.eventColor.cancel();
//   }

//   void sendBrightnes(String bright) {
//     print(this.sid);
//     this.send(this.sid, 'set_bright', bright);
//   }

//   void sendCt(String ct) {
//     this.send(this.sid, 'set_ct', ct);
//   }

//   void sendRgb(Map<String,dynamic> rgb) {
//     this.send(this.sid, 'set_rgb', rgb);
//   }

//   Map<String,dynamic> hexToRgb(String h) {
//      Map<String,dynamic> ret = new Map();

//     if (h.length == 7) {
//       int r = int.parse(h.substring(1,3),radix:16);
//       int g = int.parse(h.substring(3,5),radix:16);
//       int b = int.parse(h.substring(5,7),radix:16);
//       ret = {'red': r, 'green': g, 'blue': b};
//     }
//     return ret;
//   }

//   String rgbToHex(int r, int g, int b) {
//     String hex = '#${r.toRadixString(16).padLeft(2,'0')}${g.toRadixString(16).padLeft(2,'0')}${b.toRadixString(16).padLeft(2,'0')}';
//     print(hex);
//     return hex;
//   }
// }