import 'dart:async';
import 'dart:html';
import 'dart:convert';
import 'package:service_worker/window.dart' as sw;
import '../lib/modal.dart';
import '../lib/devicewidget.dart';

void _log(Object o) => print('  MAIN: $o');

class Page {
  Devices devices = new Devices();
  EventSource events;

  Page() {
    HttpRequest.getString('/dev/data/all').then((String resp) {
      List<dynamic> jdata = jsonDecode(resp);
      jdata.forEach((dev) {
        this.devices.register(dev, print);
      });
    });
    
    this.events = new EventSource('/stream');
    this.events.onMessage.listen((ev) {
      this.devices.refresh(ev.data);
    });
    this.events.onOpen.listen((e){
      print('conn');
      print('${this.events.url} ${this.events.readyState}');
    });
    this.events.onError.listen((er){
      print('err ${er}');
    });
  }
}

Future main() async {
  new Page();

  if (sw.isNotSupported) {
    _log('ServiceWorkers are not supported.');
    return;
  }

  await sw.register('/static/devices/sw.dart.js');
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
