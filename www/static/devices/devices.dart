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
      this.handler(e.data);
    });
  }

  void setStartTime(num start) {
    this.startTime = start;
    window.animationFrame.then(this.checkConnection);
  }

  void checkConnection(num frame) {
    print(frame);
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
  var ws;

  Lights() {
    this.loader.classes.add('show-loader');
    this.ws =
        WebSockets('ws://127.0.0.1:9000', handler: this.refreshDevicesStatus);
    this.buttons = querySelectorAll('.device button');
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
    HttpRequest.getString('/dev/data/all').then((String resp) {
      List<dynamic> jdata = jsonDecode(resp);
      Map<String, dynamic> devs = new Map();
      jdata.forEach((dev) {
        devs[dev['sid']] = dev;
      });
      this.buttons.forEach((btn) {
        btn.value = devs[btn.dataset['sid']][btn.dataset['status']];
        if (btn.value == 'on') {
          btn.classes.add('orange');
          btn.text = 'off';
        } else if (btn.value == 'off') {
          btn.classes.remove('orange');
          btn.text = 'on';
        }
      });
    });
  }

  void refreshDevicesStatus(data) async {
    try {
      Map<String, dynamic> info = json.decode(data);

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
    } catch (e) {
      print(data);
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
