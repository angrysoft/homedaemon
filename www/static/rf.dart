import "dart:html";

class Rf {
  List<Element> buttons;

  Rf() {
    buttons = querySelectorAll('.btn');
    buttons.forEach((b) {
      b.onClick.listen((Event e) {
        e.preventDefault();
        ButtonElement btn = e.target;
        String code = btn.getAttribute('data-rf-code');
        HttpRequest.request('/rf/send/${code}', method: 'POST');
      });
    });
  }
}

void main() {
  new Rf();
}