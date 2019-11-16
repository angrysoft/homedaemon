import 'dart:html';

void _log(Object o) => print('  Websocket: $o');

class WebSockets {
  DivElement loader = querySelector('#loader');
  WebSocket websock;
  String internet;
  String localnetwork;
  String urltoken;
  String secret;
  Function handler;
  num delayTime = 1000;
  num startTime;
  int curUrl = 0;
  bool secure;

  WebSockets(Map<String,dynamic> config, {Function handler = print, bool secure = false}) {
    this.internet = config['internet'];
    this.localnetwork = config['localnetwork'];
    this.handler = handler;
    this.urltoken = config['urltoken'];
    this.secret = config['secret'];
    this.connect();
  }

  void connect() {
    this.loader.classes.add('show-loader');
    this.websock = new WebSocket(this.geturl());

    this.websock.onOpen.listen((e) {
      _log('Connected!');
      if (this.secret.isNotEmpty) {
        this.send(this.secret);
      }
      this.loader.classes.remove('show-loader');
    });

    this.websock.onClose.listen((e) {
      _log('Close');
      window.animationFrame.then(this.setStartTime);
    });

    this.websock.onError.listen((_) => this.connect());

    this.websock.onMessage.listen((e) {
      this.handler(e.data);
    });
  }

  String geturl() {
    String url = '';
    Navigator nav = window.navigator;
    switch(nav.connection.type) {
      case 'wifi':
      {
        url = this.localnetwork;
      }
      break;
      case 'cellular':
      {
        url = this.internet;
      }
      break;
      default:
      {
        url = this.localnetwork;
      }
    }
    return "${url}?token=${this.urltoken}";
  }

  void setStartTime(num start) {
    this.startTime = start;
    window.animationFrame.then(this.checkConnection);
  }

  void checkConnection(num frame) {
    if (this.websock != null && this.websock.readyState == WebSocket.OPEN ||
        this.websock.readyState == WebSocket.CONNECTING) {
      return;
    } else if (frame >= (this.startTime + this.delayTime)) {
      this.startTime = frame;
      this.connect();
    }
    window.animationFrame.then(this.checkConnection);
  }

  void send(String value) {
    if (this.websock != null && this.websock.readyState == WebSocket.OPEN) {
      this.websock.send(value);
    }
  }
}