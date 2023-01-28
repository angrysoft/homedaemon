import 'dart:html';

import '../lib/modal.dart';

void main() {
  Modal devadd = new Modal.fromHtml('devadd');
  ButtonElement addbtn = querySelector('#addbtn');
  addbtn.onClick.listen((e)=> devadd.show()); 
}