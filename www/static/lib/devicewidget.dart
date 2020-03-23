import 'dart:html';
import 'dart:convert';
import 'dart:core';
import 'dart:async';
import 'modal.dart';

class Devices {
  Map<String,BaseDeviceWidget> _devices;

  Devices() {
    this._devices = new Map();
  }

  void register( Map<String,dynamic> devData, Function evSend) {
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
      case 'desklamp':
      {
        this._devices[devData['sid']] = new DeskLamp(devData, evSend);
      }
      break;
      case 'philips.light.candle':
      {
        this._devices[devData['sid']] = new PhilipsBulb(devData, evSend);
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
      case 'sensor_motion.aq2':
      {
        this._devices[devData['sid']] = new SensorMotion(devData);
      }
      break; 
      /* case 'scene':
      {
        this._devices[devData['sid']] = new Scene(devData, evSend);
      }
      break; */
    }
  }

  Future refresh(String data) async {
    try {
      print('DEBUG ${data} END');
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
    // this.channel_1.setStatus(this.devData['channel_1']);
    print("butt1 ${this.channel_1.getStatus()}");
    this.refreshStatus(devData);
    this.channel_1.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    super.refreshStatus(devData);
    if (devData.containsKey('channel_1')) {
      print("ch0 ${devData['channel_0']}");
      print("ch1 ${devData['channel_1']}");
      // this.channel_1.setStatus(devData['channel_1']);
    }
  }
}


class CtrlNeutral1 extends DeviceWidget {
  Button channel_0;

  CtrlNeutral1(Map<String,dynamic> devData, Function evSend) : super (devData, evSend) {
    this.channel_0 = new Button('channel_0', this.sid);
    // this.channel_0.setStatus(this.devData['channel_0']);
    print("butt0 ${this.channel_0}");
    this.refreshStatus(this.devData);
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
    // this.power.setStatus(this.devData['status']);
    this.refreshStatus(devData);
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


class RgbStrip extends Bslamp1 {
  RgbStrip(Map<String,dynamic> devData, Function evSend) : super(devData, evSend);
}


class Color extends Bslamp1 {
  Color(Map<String,dynamic> devData, Function evSend) : super(devData, evSend);
}


class DeskLamp extends DeviceWidget {
  Button power;
  WhiteSetButton setBtn;

  DeskLamp(Map<String,dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('power', this.sid);
    // this.power.setStatus(this.devData['power']);
    this.refreshStatus(devData);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    
    this.setBtn = new WhiteSetButton(sid);
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    if (devData.containsKey('power')) {
      this.power.setStatus(devData['power']);
    }
  }

}

class PhilipsBulb extends DeskLamp {
  PhilipsBulb(Map<String,dynamic> devData, Function evSend) : super(devData, evSend);
}


class Bslamp1 extends DeviceWidget {
  Button power;
  ColorSetButton setBtn;

  Bslamp1(Map<String, dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('power', this.sid);
    // this.power.setStatus(this.devData['power']);
    this.refreshStatus(devData);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    this.setBtn = new ColorSetButton(this.sid);
  }

  @override
  void refreshStatus(Map<String, dynamic> devData) {
    if (devData.containsKey('power')) {
      this.power.setStatus(devData['power']);
    }
  }
}

class Scene extends DeviceWidget {
  SceneButton runOn;
  SceneButton runOff;

  Scene(Map<String, dynamic> devData, Function evSend) : super(devData, evSend) {
    this.runOn = new SceneButton('sceneon', sid);
    this.runOn.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    this.runOff = new SceneButton('sceneoff', sid);
    // this.runOff.btn.onClick.listen((ev) {
    //   this.send(ev.target);
    // });
  }

  void refreshStatus(Map<String,dynamic> devData) {
    switch(devData['status']) {
      case 'on':
      {
        this.runOn.setRunning(devData['running']);
      }
      break;

      case 'off':
      {
        this.runOff.setRunning(devData['running']);
      }
      break;
    }
  }
}


class Bravia extends DeviceWidget {
  Button power;
  TvSetButton setBtn;

  Bravia(Map<String,dynamic> devData, Function evSend) : super(devData, evSend) {
    this.power = new Button('power', this.sid);
    // this.power.setStatus(this.devData['power']);
    this.refreshStatus(devData);
    this.power.btn.onClick.listen((ev) {
      this.send(ev.target);
    });
    this.setBtn = new TvSetButton(this.sid);
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
      print('RESPONSE TXT $data : ${resp.responseText} ENDTXT');
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

class SensorMotion extends ReadOnlyDevice {
  Label lux;
  Label motion;
  Label vol;
  SensorMotion(Map<String,dynamic> devData) : super(devData) {
    this.lux = new Label('lux', this.sid);
    this.motion = new Label('motion', this.sid);
    this.vol = new Label('voltage', this.sid);
    this.refreshStatus(devData);
  }

  @override
  void refreshStatus(Map<String,dynamic> devData) {
    if (devData.containsKey('when')) {
      DateTime d = DateTime.parse(devData['when']);
      this.motion.setStatus("${d.hour}:${d.minute}:${d.second}");
    }
    if (devData.containsKey('voltage')) {
      this.vol.setStatus((devData['voltage']).toString());
    }
    if (devData.containsKey('lux')) {
      this.lux.setStatus((devData['lux']).toString());
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

class SceneButton extends Button {
  SceneButton(String name, String sid) : super(name, sid);
  
  setRunning(bool running) {
    if (running) {
      this._status = true;
      this.btn.classes.add('orange');
    } else {
      this._status = false;
      this.btn.classes.remove('orange');
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

class WhiteSetButton {
  ButtonElement btn;
  WhiteSetterWindow whiteWnd;
  WhiteSetButton(String sid) {
    this.whiteWnd = new WhiteSetterWindow(sid);
    this.btn = querySelector('button.white-set-button[data-sid="${sid}"]');
    this.btn.onClick.listen((ev) {
      this.whiteWnd.showWindow();
    });
  }
}

class ColorSetButton {
  ButtonElement btn;
  ColorSetterWindow colorWnd;
  ColorSetButton(String sid) {
    this.colorWnd = new ColorSetterWindow(sid);
    this.btn = querySelector('button.color-set-button[data-sid="${sid}"]');
    this.btn.onClick.listen((ev) {
      this.colorWnd.showWindow();
    });
  }
}

class WhiteSetterWindow {
  Modal whiteWnd;
  Element back;
  String sid;
  ButtonElement btnRgb;
  RangeInputElement bright = querySelector('#white-bright');
  RangeInputElement ct = querySelector('#white-ct');
  StreamSubscription eventBright;
  StreamSubscription eventCt;
  bool current = false;

  WhiteSetterWindow(String sid) {
    this.sid = sid;
    this.whiteWnd = new Modal.fromHtml('white-set');
    this.back = querySelector('#back-white');
    this.back.onClick.listen((e) {
      this.closeWindow();
    });

    this.eventBright = this.bright.onChange.listen((e) {
      this.send('set_bright', this.bright.value);
    });

    this.eventCt = this.ct.onChange.listen((e) {
      this.send('set_ct_pc', this.ct.value);
    });

  }
  
  showWindow() {
    this.setData();
    this.current = true;
    this.whiteWnd.show();
  }

  closeWindow() {
    this.current = false;
    this.whiteWnd.hide();
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

        if (data.containsKey('ct_pc')) {
          this.ct.value = data['ct_pc'].toString();
        }
    });
  }
}

class ColorSetterWindow {
  Modal colorWnd;
  Element back;
  String sid;
  ButtonElement btnRgb;
  ButtonElement btnCt;
  RangeInputElement bright = querySelector('#color-bright');
  RangeInputElement ct = querySelector('#white-ct');
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
      this.send('set_ct_pc', this.ct.value);
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

class TvSetButton {
  ButtonElement btn;
  TvSetterWindow tvWnd;
  TvSetButton(String sid) {
    this.tvWnd = new TvSetterWindow(sid);
    this.btn = querySelector('button.tv-set-button[data-sid="${sid}"]');
    this.btn.onClick.listen((ev) {
      this.tvWnd.showWindow();
    });
  }
}

class TvSetterWindow {
  Modal tvWnd;
  Element back;
  String sid;
  bool current = false;
  
  TvSetterWindow(String sid) {
    this.sid = sid;
    this.tvWnd = new Modal.fromHtml('tv-set');
    this.back = querySelector('#back-tv');
    this.back.onClick.listen((e) {
      this.closeWindow();
    });
    querySelectorAll('#tv-set .btn').onClick.listen((Event e) => this.send(e));
  }

  showWindow() {
    this.setData();
    this.current = true;
    this.tvWnd.show();
  }

  closeWindow() {
    this.current = false;
    this.tvWnd.hide();
  }

  Future<void> send(Event e) async {
    ButtonElement btn = e.target;
    Map<String, dynamic> msg = new Map();
    msg['cmd'] = 'write';
    msg['sid'] = 'tv01';
    msg['data'] = {'button': btn.dataset['btn']};
    String data = json.encode(msg);
    await HttpRequest.request('/dev/write', method: 'POST', sendData: data); 
  }

  void setData() {

  }
}