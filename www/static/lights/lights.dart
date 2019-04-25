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
      print('<${e.data}');
    });
  }

  void setStartTime(num start) {
    this.startTime = start;
    window.animationFrame.then(this.checkConnection);
  }

  void checkConnection(num frame) {
    print('${frame} , ${this.startTime + this.delayTime}');
    if (this.websock != null && this.websock.readyState == WebSocket.OPEN ||
        this.websock.readyState == WebSocket.CONNECTING) {
      return;
    } else if (frame >= (this.startTime + this.delayTime)) {
      print('reconecting');
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

class Lights {
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
        print('==${info} ${btn.dataset['status']}');
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

    // data.append('sid', sid);
    // data.append('cmdname', cmdname);
    // data.append('cmdvalue', cmdvalue);
    // data.append('model', model);
    // HttpRequest.request('/dev/write', method: 'POST', sendData: data)
    // .then((HttpRequest resp) {
    // this.refresDevicesStatus();
    // });
  }
}

class TabButtons {
  String tab = '0';

  TabButtons() {
    DivElement buttons = querySelector('.buttons');
    for (int j = 1; j < 5; j++) {
      ButtonElement btnOn = new ButtonElement();
      btnOn
        ..text = j.toString()
        ..className = 'btn green'
        ..dataset['btn'] = j.toString()
        ..dataset['btnFunc'] = 'on'
        ..onClick.listen((Event e) => this.clickBtn(e));
      ButtonElement btnOff = new ButtonElement();
      btnOff
        ..text = j.toString()
        ..className = 'btn red'
        ..dataset['btn'] = j.toString()
        ..dataset['btnFunc'] = 'off'
        ..onClick.listen((Event e) => this.clickBtn(e));

      DivElement col1 = new DivElement();
      col1
        ..className = 'col-xs'
        ..append(btnOn);
      DivElement col2 = new DivElement();
      col2
        ..className = 'col-xs'
        ..append(btnOff);
      DivElement row = new DivElement();
      row
        ..className = 'row center-xs txt-center'
        ..append(col1)
        ..append(col2);
      buttons.append(row);
    }
    List<Element> tabBtn = querySelectorAll('.tab-btn');
    tabBtn.forEach((t) {
      t.onClick.listen((Event e) => this.changeTab(e));
    });
    querySelectorAll('.btn-all').onClick.listen((Event e) => this.clickBtn(e));
  }

  void changeTab(Event e) {
    ButtonElement tabBtn = e.target;
    List<Element> active = querySelectorAll('.active');
    active.forEach((a) {
      a.classes.remove('active');
    });
    tabBtn.classes.add('active');
    this.tab = tabBtn.dataset['tab'];
  }

  void clickBtn(Event e) {
    ButtonElement btn = e.target;
    String btnNo = '';
    if (btn.dataset['btn'] != 'all') {
      int n = int.parse(btn.dataset['btn']) + int.parse(this.tab);
      btnNo = n.toString();
    } else {
      btnNo = btn.dataset['btn'];
    }
    HttpRequest.request(
            '/rf/pilot/button/${btnNo}?func=${btn.dataset['btnFunc']}',
            method: 'POST')
        .then((HttpRequest resp) {
      print(resp);
    });
  }
}

Future main() async {
  new Lights();

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
