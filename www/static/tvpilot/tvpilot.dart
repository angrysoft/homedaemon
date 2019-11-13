import 'dart:async';
import 'dart:html';
import 'dart:convert';
import '../lib/websock.dart';

import 'package:service_worker/window.dart' as sw;

void _log(Object o) => print('  MAIN: $o');

class TvButtons {
  WebSockets ws;
  Map<String, dynamic> config;

  TvButtons() {
    this.connectWs();
    querySelectorAll('.btn').onClick.listen((Event e) => this.clickBtn(e));
  }

  void connectWs() {
    HttpRequest.getString('/dev/config').then((String resp) {
      this.config = jsonDecode(resp);
      this.ws = WebSockets(this.config, handler: this.onWsockMsg);
    });
  }

  void onWsockMsg(String msg) {
    return null;
  }

  void clickBtn(Event e) {
    ButtonElement btn = e.target;
    Map<String, dynamic> msg = new Map();
    msg['cmd'] = 'write';
    msg['sid'] = 'tv01';
    msg['data'] = {'button': btn.dataset['btn']};
    print(msg);
    this.ws.send(json.encode(msg));
  }

}

Future main() async {
  new TvButtons();

  if (sw.isNotSupported) {
    _log('ServiceWorkers are not supported.');
    return;
  }

  await sw.register('/static/tvpilot/sw.dart.js');
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