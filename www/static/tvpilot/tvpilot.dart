import 'dart:async';
import 'dart:html';
import 'dart:convert';
import 'package:service_worker/window.dart' as sw;

void _log(Object o) => print('  MAIN: $o');

class TvButtons {
  Map<String, dynamic> config;

  TvButtons() {
    querySelectorAll('.btn').onClick.listen((Event e) => this.clickBtn(e));
  }

  Future<void> clickBtn(Event e) async {
    ButtonElement btn = e.target;
    Map<String, dynamic> msg = new Map();
    msg['cmd'] = 'write';
    msg['sid'] = 'tv01';
    msg['data'] = {'button': btn.dataset['btn']};
    String data = json.encode(msg);
    await HttpRequest.request('/dev/write', method: 'POST', sendData: data); 
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
    _log('Error: Adding push subscription failed. ${e}');
    _log('       See github.com/isoos/service_worker/issues/10');
  }
}