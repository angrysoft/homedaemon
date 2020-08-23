import 'dart:html';

Future<void> sendCmd(String cmd) async {
  DivElement spinner = querySelector('.loader-wraper');
  spinner.classes.add('show-loader');
  await HttpRequest.request('/system',
          method: 'POST', sendData: '{"cmd": "$cmd"}')
      .then((HttpRequest resp) {
    print('$cmd : ${resp.responseText}');
    spinner.classes.remove('show-loader');
  });
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
