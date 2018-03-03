import 'dart:async';
import 'dart:html';

import 'package:service_worker/window.dart' as sw;

void _log(Object o) => print('  MAIN: $o');

class TabButtons {
  String tab = '0';

  TabButtons() {
    DivElement buttons = querySelector('.buttons');
    for (int j = 1; j < 5; j++) {
        ButtonElement btnOn = new ButtonElement();
        btnOn..text = j.toString()
        ..className = 'btn green'
        ..dataset['btn'] = j.toString()
        ..dataset['btnFunc'] = 'on'
        ..onClick.listen((Event e) => this.clickBtn(e));
        ButtonElement btnOff = new ButtonElement();
        btnOff..text = j.toString()
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
    HttpRequest.request('/rf/pilot/button/${btnNo}?func=${btn.dataset['btnFunc']}', method: 'POST')
    .then((HttpRequest resp) {
      print(resp);
    });
  }
}

Future main() async {
  new TabButtons();

  if (sw.isNotSupported) {
    _log('ServiceWorkers are not supported.');
    return;
  }

  await sw.register('/static/sw.dart.js');
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
