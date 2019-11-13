import 'dart:html';

void _log(Object o) => print('  Websocket: $o');

class WebSockets {
  DivElement loader = querySelector('#loader');
  WebSocket websock;
  List<String> urls;
  String urltoken;
  String secret;
  Function handler;
  num delayTime = 1000;
  num startTime;
  int curUrl = 0;
  bool secure;

  WebSockets(Map<String,dynamic> config, {Function handler = print, bool secure = false}) {
    this.urls = new List();
    config['servers'].forEach((e){
      this.urls.add(e);
    });
    
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
    if (this.curUrl >= this.urls.length) {
      this.curUrl = 0;
    }
    String url = this.urls[this.curUrl];
    this.curUrl++;
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