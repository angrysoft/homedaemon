import "dart:html";


class Led {
  InputElement ledPicker;
  ButtonElement btnOff;

  Led() {

    this.ledPicker = querySelector('#ledPicker');
    this.ledPicker.onChange.listen((e) {
      String rgbColor = this.hexToRgb(this.ledPicker.value);
      HttpRequest.request('/leds/changeColor/${rgbColor}', method: 'POST');
    });
    this.btnOff = querySelector('#btn-off');
    this.btnOff.onClick.listen((Event e) {
      HttpRequest.request('/leds/changeColor/0.0.0', method: 'POST');
    });
  }

  String hexToRgb(String hexCode) {
    if (hexCode.startsWith('#')) {
      hexCode = hexCode.substring(1);
    }
    List<String> hexDigits = hexCode.split('');
    int r = int.parse(hexDigits.sublist(0, 2).join(), radix: 16);
    int g = int.parse(hexDigits.sublist(2, 4).join(), radix: 16);
    int b = int.parse(hexDigits.sublist(4).join(), radix: 16);
    return "${r}.${g}.${b}";
  }
}


void main() {
  new Led();
}