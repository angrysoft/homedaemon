import 'dart:async';
import 'dart:html';

import 'package:service_worker/window.dart' as sw;

void _log(Object o) => print('  MAIN: $o');

class Led {
  InputElement inputRed;
  InputElement inputGreen;
  InputElement inputBlue;
  InputElement inputDimm;
  ButtonElement btnOff;
  ButtonElement btnSet;

  Led() {
    inputRed = querySelector('#red');
    inputGreen = querySelector('#green');
    inputBlue = querySelector('#blue');
    inputDimm = querySelector('#dimm');
    btnOff = querySelector('#btn-off');
    btnSet = querySelector('#btn-set');
    
    this.inputRed.onChange.listen((e) => this.setColorPreview());
    this.inputGreen.onChange.listen((e) => this.setColorPreview());
    this.inputBlue.onChange.listen((e) => this.setColorPreview());

    this.btnSet.onClick.listen((Event e) {
      String rgbColor = this.getColor();
       HttpRequest.request('/leds/changeColor/${rgbColor}', method: 'POST');
    });

    this.btnOff.onClick.listen((Event e) {
      HttpRequest.request('/leds/changeColor/0.0.0', method: 'POST');
    });
  }

  String getColor() {
    return "${inputRed.value}.${inputGreen.value}.${inputBlue.value}.${inputDimm.value}";
  }

  void setColorPreview() {
    this.btnSet.style.background = "rgb(${inputRed.value},${inputGreen.value},${inputBlue.value})";
  }

//  String hexToRgb(String hexCode) {
//    if (hexCode.startsWith('#')) {
//      hexCode = hexCode.substring(1);
//    }
//    List<String> hexDigits = hexCode.split('');
//    int r = int.parse(hexDigits.sublist(0, 2).join(), radix: 16);
//    int g = int.parse(hexDigits.sublist(2, 4).join(), radix: 16);
//    int b = int.parse(hexDigits.sublist(4).join(), radix: 16);
//    return "${r}.${g}.${b}";
//  }
}

Future main() async {
  new Led();

  if (sw.isNotSupported) {
    _log('ServiceWorkers are not supported.');
    return;
  }

  await sw.register('/static/ledpilot/sw.dart.js');
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