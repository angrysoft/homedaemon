import 'dart:html';

void login() {
  InputElement inputUser = querySelector('#user');
  InputElement inputPasswd = querySelector('#passwd');
  inputUser.setCustomValidity('');
  if (! inputUser.checkValidity()) {
    inputUser.reportValidity();
    return;
  }
  else if (! inputPasswd.checkValidity()) {
    inputPasswd.reportValidity();
    return;
  }
  FormData data = new FormData();
    data.append('user', inputUser.value);
    data.append('passwd', inputPasswd.value);
    HttpRequest.request('/admin/login', method: 'POST', sendData: data)
      .then((HttpRequest resp) {
        if (resp.responseText == 'ko') {
          inputUser.setCustomValidity('Wrong user or password');
          inputUser.reportValidity();
        } else {
          window.location.replace(resp.responseText);
        }
      });
}

void main() {
  window.onKeyUp.listen((KeyboardEvent key) {
          if (key.keyCode == 13) {
            login();
          }
        });
  ButtonElement btnLogin = querySelector('#btn-login');
  btnLogin.onClick.listen((e){
    // e.preventDefault();
    login();
  }); 
}
