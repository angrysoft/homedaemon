function makeHttpObject() {
  try {return new XMLHttpRequest();}
  catch (error) {}
  try {return new ActiveXObject("Msxml2.XMLHTTP");}
  catch (error) {}
  try {return new ActiveXObject("Microsoft.XMLHTTP");}
  catch (error) {}

  throw new Error("Could not create HTTP request object.");
}

function sendColor(c) {
  var request = makeHttpObject();
  var url = 'leds?'+ 'name' + '=' + c;
  request.open("POST", url, true);
  request.send(null);
}

function sendButton(b,s) {
  var request = makeHttpObject();
  var url = 'buttons?'+ b + '=' + s;
  request.open("POST", url, true);
  request.send(null);
}

function sendCommand(c,s) {
  var request = makeHttpObject();
  var url = 'buttons?'+ c + '=' + s;
  request.open("POST", url, true);
  request.send(null);
}

function sendScene(s) {
  var request = makeHttpObject();
  var url = 'scenes?'+ s;
  request.open("POST", url, true);
  request.send(null);
}

function sendRGB() {
    var r = document.getElementById("r");
    var g = document.getElementById("g");
    var b = document.getElementById("b");
    var rgb = r.value + '.' + g.value + '.' + b.value;
    var request = makeHttpObject();
    var url = 'leds?'+ 'RGB' + '=' + rgb;
    request.open("POST", url, true);
    request.send(null);
}

function setRGB() {
    var r = document.getElementById("r"),
    g = document.getElementById("g"),
    b = document.getElementById("b"),
    sentBtn = document.getElementById("sentBtn"),
    rgbval =  r.value + ',' + g.value + ',' + b.value,
    rgbTxt = r.value + '.' + g.value + '.' + b.value,
    colorBox = document.getElementById("RGB");
    sentBtn.innerHTML = "Sent RGB : " + rgbTxt;
    sentBtn.style.backgroundColor= "rgb(" + rgbval + ")";
    if ((parseInt(r.value) >= 150) || (parseInt(g.value) >= 150) ) {
        sentBtn.style.color="black";
    } else {
        sentBtn.style.color="white";
    }
}