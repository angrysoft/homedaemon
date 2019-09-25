import 'dart:async';
import 'dart:html';
import 'dart:convert';
import 'package:service_worker/window.dart' as sw;
import '../lib/modal.dart';

void _log(Object o) => print('  MAIN: $o');

class WebSockets {
  WebSocket websock;
  String url;
  Function handler;
  num delayTime = 1000;
  num startTime;

  WebSockets(String _url, {Function handler = print}) {
    this.url = _url;
    this.handler = handler;
    this.connect();
  }

  void connect() {
    this.websock = new WebSocket(this.url);

    this.websock.onOpen.listen((e) {
      print('Connected!');
    });

    this.websock.onClose.listen((e) {
      print('Close');
      window.animationFrame.then(this.setStartTime);
    });

    this.websock.onError.listen((_) => print('Error opening connection.'));

    this.websock.onMessage.listen((e) {
      this.handler(e.data);
    });
  }

  void setStartTime(num start) {
    this.startTime = start;
    window.animationFrame.then(this.checkConnection);
  }

  void checkConnection(num frame) {
    if (this.websock != null && this.websock.readyState == WebSocket.OPEN ||
        this.websock.readyState == WebSocket.CONNECTING) {
      return;
    } else if (frame >= (this.startTime + this.delayTime)) {
      this.startTime = frame;
      this.connect();
    }
    window.animationFrame.then(this.checkConnection);
  }

  void send(String value) {
    if (this.websock != null && this.websock.readyState == WebSocket.OPEN) {
      this.websock.send(value);
    }
  }
}

class Devices {
  DivElement loader = querySelector('#loader');
  List<ButtonElement> buttons = new List();
  List<ButtonElement> colorSetButtons = new List();
  Modal colorSet;
  Map<String, List> deviceStatus = new Map();
  Map<String, dynamic> config = new Map();
  WebSockets ws;
  Element back;
  Tabs tabs = new Tabs();
  ColorSetter colsetter;

  Devices() {
    this.loader.classes.add('show-loader');
    this.connectWs();
    this.buttons = querySelectorAll('button.device-status');
    this.colorSetButtons = querySelectorAll('.color-set-button');
    this.colorSet = new Modal.fromHtml('color-set');
    this.back = querySelector('#back');
    
    this.getDevicesStatus();
    // window.onPageShow.listen((event) {
      // this.getDevicesStatus();
    // });

    querySelectorAll('.device-status').forEach((dev) {
      if (this.deviceStatus.containsKey(dev.dataset['sid'])) {
        this.deviceStatus[dev.dataset['sid']].add(dev);
      } else {
        this.deviceStatus[dev.dataset['sid']] = [dev];
      }
    });

    this.back.onClick.listen((e) {
      this.colorSet.hide();
      this.tabs.enableTouch = true;
    });

    this.buttons.forEach((btn) {
      btn.onClick.listen((event) {
        event.preventDefault();
        ButtonElement b = event.target;
        String cmd;
        if (b.dataset.containsKey('cmd')) {
          cmd = b.dataset['cmd'];
        } else {
          cmd = b.dataset['status'];
        }
        this.sendWriteCmd(b.dataset['sid'], cmd, b.value);
      });
    });

    this.colorSetButtons.forEach((btn) {
      btn.onClick.listen((event) {
        this.tabs.enableTouch = false;
        HttpRequest.getString('/dev/data/${btn.dataset['sid']}').then((String resp) {
          var data = jsonDecode(resp);
          if (data.containsKey('sid')) {
            this.colsetter = new ColorSetter(data, this.sendWriteCmd);
          }
        });
        this.colorSet.show();
      });
    });
    this.loader.classes.remove('show-loader');
  }


  void connectWs() {
    HttpRequest.getString('/dev/config').then((String resp) {
      this.config = jsonDecode(resp);
      this.ws = WebSockets("ws://${this.config['ip']}:${this.config['port']}", handler: this.refreshDevicesStatus);
      });
  }

  void getDevicesStatus() {
    HttpRequest.getString('/dev/data/all').then((String resp) {
      List<dynamic> jdata = jsonDecode(resp);
      jdata.forEach((dev) {
        if (this.deviceStatus.containsKey(dev['sid'])) {
          var devs = this.deviceStatus[dev['sid']];
          devs.forEach((d) {
            if (d is ButtonElement) {
              this.updateButton(d, dev);
            } else {
              if (dev.containsKey(d.dataset['status'])) {
                this.updateElement(d, dev);
              }
            }
          });
        }
      });
    });
  }

  void refreshDevicesStatus(data) async {
    try {
      Map<String, dynamic> info = json.decode(data);

      if (this.deviceStatus.containsKey(info['sid']) &&
          info.containsKey('data')) {
        var devs = this.deviceStatus[info['sid']];
        
        devs.forEach((d) {
          if (d is ButtonElement) {
            this.updateButton(d, info['data']);
          } else {
            if (info['data'].containsKey(d.dataset['status'])) {
              this.updateElement(d, info['data']);
            }
          }
        });
      }
    } catch (e) {
      print('error: ${data}');
    }
  }

  void updateButton(ButtonElement btn, Map dev) {
    switch(dev[btn.dataset['status']]) { 
      case "on": {
        btn.classes.add('orange');
        btn.text = 'off';
        btn.value = 'off';
      } 
      break; 
     
      case "off": {
        btn.classes.remove('orange');
        btn.text = 'on';
        btn.value = 'on';
      } 
      break;
   }   
  }

  void updateElement(Element el, Map data) {
    String status = el.dataset['status'];
    
    switch (status) {
      case 'temperature':
        {
          el.text = "${(int.parse(data[status]) / 100).ceil()} C";
        }
        break;

      case 'humidity':
        {
          el.text = "${(int.parse(data[status]) / 100).ceil()} %";
        }
        break;
      
      case 'pressure':
        {
          el.text = "${(int.parse(data[status]) / 1000).ceil()} kPa";
        }
        break;

      default:
        {
          el.text = data[el.dataset['status']].toString();
        }
        break;
    }
  }

  void sendWriteCmd(String sid, String cmdname, dynamic cmdvalue) {
    Map<String, dynamic> msg = new Map();
    msg['cmd'] = 'write';
    msg['sid'] = sid;
    msg['data'] = {cmdname: cmdvalue};
    print(msg);
    this.ws.send(json.encode(msg));
  }
}

class ColorSetter {
  String sid;
  ButtonElement btnRgb;
  ButtonElement btnCt;
  DivElement rgbTab;
  DivElement ctTab;
  Map<String, dynamic> lampdata;
  RangeInputElement bright = querySelector('#bright');
  RangeInputElement ct = querySelector('#ct');
  InputElement color = querySelector('#color-picker');
  Function send;

  ColorSetter(Map<String,dynamic> data, Function send) {
    this.sid = data['sid'];
    this.lampdata = data;
    this.send = send;

    print(data);

    this.bright.onChange.listen((e) {
      this.sendBrightnes(this.bright.value);
    });

    this.ct.onChange.listen((e) {
      this.sendCt(this.ct.value);
    });

    this.color.onChange.listen((e) {
      this.sendRgb(this.hexToRgb(this.color.value));
    });

    if (this.lampdata.containsKey('bright')) {
      this.bright.value = this.lampdata['bright'].toString();
    }

    if (this.lampdata.containsKey('ct')) {
      this.ct.value = this.lampdata['ct'].toString();
    }

    if (this.lampdata.containsKey('rgb')) {
      int rgbint;
      if (this.lampdata['rgb'] is int) {
        rgbint = this.lampdata['rgb'];
      } else {
        rgbint = int.parse(this.lampdata['rgb']);
      }
      int b =  rgbint & 255;
      int g = (rgbint >> 8) & 255;
      int r =   (rgbint >> 16) & 255;
      print('${r}.${g}.${b}');
      this.color.value = this.rgbToHex(r, g, b);
    } else if (this.lampdata.containsKey('red') && this.lampdata.containsKey('green') && this.lampdata.containsKey('blue')) {
      this.color.value = this.rgbToHex(this.lampdata['red'], this.lampdata['green'], this.lampdata['blue']);
    }


    this.btnCt = querySelector('#ct-btn');
    this.btnRgb = querySelector('#rgb-btn');
    this.rgbTab = querySelector('#rgb-tab');
    this.ctTab = querySelector('#ct-tab');
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
  }

  void sendBrightnes(String bright) {
    this.send(this.sid, 'set_bright', bright);
  }

  void sendCt(String ct) {
    this.send(this.sid, 'set_ct', ct);
  }

  void sendRgb(Map<String,dynamic> rgb) {
    this.send(this.sid, 'set_rgb', rgb);
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

  String rgbToHex(int r, int g, int b) {
    String hex = '#${r.toRadixString(16).padLeft(2,'0')}${g.toRadixString(16).padLeft(2,'0')}${b.toRadixString(16).padLeft(2,'0')}';
    print(hex);
    return hex;
  }
}

class Tabs {
  num currentTab = 0;
  num lastTab;
  List<DivElement> tabs;
  bool _enable = true;

  Tabs() {
    tabs = querySelectorAll('.tab');
    this.lastTab = tabs.length - 1;
    Point tstart;
    Point tend;
    if (tabs.isNotEmpty) {
      this.currentTab = 0;

      if (window.localStorage.containsKey("currentTab")) {
        this.currentTab = int.parse(window.localStorage["currentTab"]);
      }

      this.changeTab(this.currentTab);
    }

    window.onTouchStart.listen((e) {
      tstart = new Point(e.touches[0].client.x, 0);
    });

    window.onTouchEnd.listen((e) {
      if (this.enableTouch) {
        tend = Point(e.changedTouches[0].client.x, 0);
        num move = tstart.x - tend.x;
        if (tend.distanceTo(tstart) > 100) {
          if (move > 0) {
            this.swipeLeft();
          } else {
            this.swipeRight();
          }
        }
      }
    });
  }

  bool get enableTouch {
    return this._enable;
  }

  void set enableTouch(bool value) {
    this._enable = value;
  }

  void swipeLeft() {
    num nextTab = this.currentTab + 1;
    if (this.lastTab >= nextTab) {
      this.changeTab(nextTab);
    } else {
      this.changeTab(0);
    }
  }

  void swipeRight() {
    num nextTab = this.currentTab - 1;
    if (nextTab >= 0) {
      this.changeTab(nextTab);
    } else {
      this.changeTab(this.lastTab);
    }
  }

  void changeTab(num tab) {
    List<Element> active = querySelectorAll('.active');
    active.forEach((a) {
      a.classes.remove('active');
    });
    tabs[tab].classes.add('active');
    this.currentTab = tab;
    window.localStorage['currentTab'] = this.currentTab.toString();
  }
}

Future main() async {
  new Devices();

  if (sw.isNotSupported) {
    _log('ServiceWorkers are not supported.');
    return;
  }

  await sw.register('/static/rfpilot/sw.dart.js');
  _log('registered');

  sw.ServiceWorkerRegistration registration = await sw.ready;
  _log('ready');

  sw.onMessage.listen((MessageEvent event) {
    _log('reply received: ${event.data}');
  });

  var message = 'Sample message: ${new DateTime.now()}';
  _log('Sending message: `$message`');
  registration.active.postMessage(message);
  _log('Message sent: `$message`');

  try {
    var subs = await registration.pushManager
        .subscribe(new sw.PushSubscriptionOptions(userVisibleOnly: true));
    _log('endpoint: ${subs.endpoint}');
  } on DomException catch (e) {
    _log('Error: Adding push subscription failed.');
    _log('       See github.com/isoos/service_worker/issues/10');
  }
}
