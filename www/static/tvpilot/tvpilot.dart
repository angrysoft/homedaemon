import 'dart:async';
import 'dart:html';

import 'package:service_worker/window.dart' as sw;

void _log(Object o) => print('  MAIN: $o');

class TvButtons {

  TvButtons() {
    querySelectorAll('.btn').onClick.listen((Event e) => this.clickBtn(e));
  }

  void clickBtn(Event e) {
    ButtonElement btn = e.target;
    HttpRequest.request('/tv/button/${btn.dataset['btn']}', method: 'POST');
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