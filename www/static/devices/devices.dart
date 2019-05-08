import 'dart:async';
import 'dart:html';
import 'dart:convert';

import 'package:service_worker/window.dart' as sw;

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
      print("< ${e.data}");
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
  List<Element> deviceStatusList = new List();
  Map<String, List> deviceStatus = new Map();
  var ws;

  Devices() {
    this.loader.classes.add('show-loader');
    this.ws =
        WebSockets('ws://192.168.1.4:9000', handler: this.refreshDevicesStatus);
    this.buttons = querySelectorAll('.device button');
    this.deviceStatusList = querySelectorAll('.device-status');
    this.getDevicesStatus();

    this.buttons.forEach((btn) {
      btn.onClick.listen((event) {
        event.preventDefault();
        ButtonElement b = event.target;
        String val = 'off';
        if (b.value == 'off') {
          val = 'on';
        }
        String cmd;
        if (b.dataset.containsKey('cmd')) {
          cmd = b.dataset['cmd'];
        } else {
          cmd = b.dataset['status'];
        }
        this.sendWriteCmd(b.dataset['sid'], b.dataset['model'], cmd, val);
      });
    });
    this.loader.classes.remove('show-loader');
  }

  void getDevicesStatus() {
    this.deviceStatusList.forEach((dev) {
      if (this.deviceStatus.containsKey(dev.dataset['sid'])) {
        this.deviceStatus[dev.dataset['sid']].add(dev);
      } else {
        this.deviceStatus[dev.dataset['sid']] = [dev];
      }
    });
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
      print(info);
      if (this.deviceStatus.containsKey(info['sid']) &&
          info.containsKey('data')) {
        var devs = this.deviceStatus[info['sid']];
        devs.forEach((d) {
          if (d is ButtonElement) {
            this.updateButton(d, info['data']);
          } else {
            if (info['data'].containsKey(d.dataset['status'])) {
              //d.text = info['data'][d.dataset['status']].toString();
              this.updateElement(d, info['data']);
            }
          }
        });
      }
      /*
      for (ButtonElement btn in this.buttons) {
        if (btn.dataset['sid'] == info['sid']) {
          Map<String, dynamic> data = info['data'];
          if (data.containsKey(btn.dataset['status'])) {
            btn.value = data[btn.dataset['status']];
            if (btn.value == 'on') {
              btn.classes.add('orange');
              btn.text = 'off';
            } else if (btn.value == 'off') {
              btn.classes.remove('orange');
              btn.text = 'on';
            }
            break;
          }
        }
      }
      */
    } catch (e) {
      print(data);
    }
  }

  void updateButton(ButtonElement btn, Map dev) {
    btn.value = dev[btn.dataset['status']];
    if (btn.value == 'on') {
      btn.classes.add('orange');
      btn.text = 'off';
    } else if (btn.value == 'off') {
      btn.classes.remove('orange');
      btn.text = 'on';
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

  void sendWriteCmd(String sid, String model, String cmdname, String cmdvalue) {
    Map<String, dynamic> msg = new Map();
    msg['cmd'] = 'write';
    msg['model'] = model;
    msg['sid'] = sid;
    msg['data'] = {cmdname: cmdvalue};
    this.ws.send(json.encode(msg));
  }
}

class Tabs {
  num currentTab = 0;
  num lastTab;
  List<DivElement> tabs;

  Tabs() {
    tabs = querySelectorAll('.tab');
    this.lastTab = tabs.length - 1;
    Point tstart;
    Point tend;
    if (tabs.isNotEmpty) {
      this.currentTab = 0;
      this.changeTab(this.currentTab);
    }

    window.onTouchStart.listen((e) {
      tstart = new Point(e.touches[0].client.x, 0);
    });

    window.onTouchEnd.listen((e) {
      tend = Point(e.changedTouches[0].client.x, 0);
      num move = tstart.x - tend.x;
      if (tend.distanceTo(tstart) > 100) {
        if (move > 0) {
          this.swipeLeft();
        } else {
          this.swipeRight();
        }
      }
    });
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
  }
}

Future main() async {
  new Devices();
  new Tabs();

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
