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
  ButtonElement btnAdd;
  ButtonElement btnColor1;
  ButtonElement btnColor2;
  ButtonElement btnColor3;
  ButtonElement btnColor4;
  ButtonElement btnColor5;
  List<ButtonElement> btns;

  Led() {
    inputRed = querySelector('#red');
    inputGreen = querySelector('#green');
    inputBlue = querySelector('#blue');
    inputDimm = querySelector('#dimm');
    btnOff = querySelector('#btn-off');
    btnSet = querySelector('#btn-set');
    btnAdd = querySelector('#btn-add');
    btnColor1 = querySelector('#color1');
    btnColor2 = querySelector('#color2');
    btnColor3 = querySelector('#color3');
    btnColor4 = querySelector('#color4');
    btnColor5 = querySelector('#color5');
    HttpRequest.getString('/leds/color').then((String ret) {
      if (ret.isNotEmpty) {
        List<String> colors = ret.split('.');
        this.inputRed.value = colors[0];
        this.inputGreen.value = colors[1];
        this.inputBlue.value = colors[2];
        this.inputDimm.value = colors[3];
      }
    })
    .catchError((Error error) {
      print(error.toString());
    });


    btns = [btnColor1, btnColor2, btnColor3, btnColor4, btnColor5];
    this.updateFavorite();
    
    this.inputRed.onChange.listen((e) => this.setColorPreview());
    this.inputGreen.onChange.listen((e) => this.setColorPreview());
    this.inputBlue.onChange.listen((e) => this.setColorPreview());

    this.btnSet.onClick.listen((Event e) {
      String rgbColor = this.getColor();
      String dimmer = this.getDimmer();
       HttpRequest.request('/leds/changeColor/${rgbColor}.${dimmer}', method: 'POST');
    });

    this.btnAdd.onClick.listen((Event e) {
      this.addToFavorite();
      this.updateFavorite();
    });

    this.btnOff.onClick.listen((Event e) {
      HttpRequest.request('/leds/changeColor/0.0.0', method: 'POST');
    });
    
    btns.forEach((Element btn) {
      btn.onClick.listen((Event e) => this.sendFavoriteColor(e));
    });
  }

  void addToFavorite() {
    window.localStorage['color1'] = window.localStorage['color2'];
    window.localStorage['color2'] = window.localStorage['color3'];
    window.localStorage['color3'] = window.localStorage['color4'];
    window.localStorage['color4'] = window.localStorage['color5'];
    window.localStorage['color5'] = this.getColor();
    window.localStorage['dimm1'] = window.localStorage['dimm2'];
    window.localStorage['dimm2'] = window.localStorage['dimm3'];
    window.localStorage['dimm3'] = window.localStorage['dimm4'];
    window.localStorage['dimm4'] = window.localStorage['dimm5'];
    window.localStorage['dimm5'] = this.getDimmer();
  }

  void updateFavorite() {
    for (int i = 1; i < 6; i++) {
      print("updateing ${i}");
      String color = "0.0.0";
      String dimmer = "0";
      if (window.localStorage.containsKey("color${i}")) {
        color = window.localStorage["color${i}"];
      }
      if (window.localStorage.containsKey("dimm${i}")) {
        dimmer = window.localStorage["dimm${i}"];
      }
      this.btns[i-1].dataset['color'] = color;
      this.btns[i-1].dataset['dimmer'] = dimmer;
      this.btns[i-1].style.background = "rgb(${color.replaceAll('.', ',')})";
    }
  }
  
  void sendFavoriteColor(Event e) {
    ButtonElement btn = e.target;
     HttpRequest.request('/leds/changeColor/${btn.dataset['color']}.${btn.dataset['dimmer']}',
         method: 'POST');
  }

  String getColor() {
    return "${inputRed.value}.${inputGreen.value}.${inputBlue.value}";
  }

  String getDimmer() {
    return "${inputDimm.value}";
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