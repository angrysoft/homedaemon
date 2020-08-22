import 'dart:html';

void sendCmd(String cmd) {
  print(cmd);
}

void main() {
  List<ButtonElement> buttonList = querySelectorAll('button');
  buttonList.forEach((element) {
    ButtonElement btn = element;
    btn.onClick.listen((event) {
      sendCmd(btn.dataset['cmd']);
    });
  });
}
