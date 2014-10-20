#include "Controller.h"




RGBdriver Driver(CLK,DIO);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
RCSwitch wSwitch = RCSwitch();

/* 
 * Constructor
 */
const byte LED_PIN = 13;

Controller::Controller() {
	pinMode(LED_PIN,OUTPUT);
	//Serial.begin(9600);
	this->inS.reserve(200);
}

void Controller::setupCtrl() {
	//RemoteReceiver::init(0, 3, getCode);
	this->rgbLed("0.0.0");
	wSwitch.enableTransmit(WIRELESS_TRANSMITER_PIN);
}


/*
 * Sending IR signal
 */

int Controller::sendIR(String code) {
	Serial.print("Sending signal IR : ");
	Serial.println(code);
	/*	code  mode.code
		mode = sony,panasonic,raw,jvc.....
		code = ir code
	*/
	return 0;
}


/*
 * Sending wireless singal 433Mhz
 */

int Controller::sendWireless(String code) {
	//code.protocol
	Serial.print("Sendign wirless :  ");
 	Serial.println(code);
	String tmp = "";
	//code to send
	unsigned long sendCode;
	//protocol
	int p = 1;
	//bit length
	int bit = 24;
	//get valu form code
	int idx = code.indexOf('.');
	tmp = code.substring(0,idx);
	sendCode = tmp.toInt();
	tmp = code.substring(idx+1);
	p = tmp.toInt();
	
	if ( p == 1) {
		bit = 24;
		wSwitch.setProtocol(1);
		wSwitch.setPulseLength(203);
		wSwitch.setRepeatTransmit(5);
		wSwitch.send(sendCode,24);
	} else if ( p == 2) {
		bit = 32;
		wSwitch.setProtocol(2);
		wSwitch.send(sendCode,32);
	}
	
	return 0;
}

int Controller::getCode(unsigned long receivedCode, unsigned int period) {
    Serial.print("Code: ");
    Serial.print(receivedCode);
    Serial.print(", period duration: ");
    Serial.print(period);
    Serial.println("us.");
	
}

/*
 * Get temperature from sensor
 */

int Controller::getTemp(int num) {
	// T.thermometr_num.temp
	sensors.requestTemperatures();
	delay(50);
	Serial.print("T.");
	Serial.print(num);
	Serial.print('.');
	Serial.println(sensors.getTempCByIndex(num));
	return 0;
}

/*
 * Get the light sensor state
 */
int Controller::getLight(int num) {
	int light = 0;
	for ( int i = 0; i<=2; i++) {
		light += analogRead(LIGHTPIN);
	}
	light = light/3;
	Serial.print("L.");
	Serial.print(num);
	Serial.print('.');
	Serial.println(light);
	return light; 
}

void Controller::rgbLed (String colors) {
	int red   = 0;
	int green = 0;
	int blue  = 0;
	Serial.println("color : "+colors);
	int idx = colors.indexOf('.');
	int idxOld = idx+1;
	//if (idx == -1) {return};
	String tmp;
	//Red
	tmp = colors.substring(0, idx);
	Serial.println(tmp);
	red = tmp.toInt();
	//Green
	idx = colors.indexOf('.',idxOld);
	tmp = colors.substring(idxOld,idx);
	Serial.println(tmp);
	green = tmp.toInt();
	//Blue
	tmp = colors.substring(idx+1);
	Serial.println(tmp);
	blue = tmp.toInt();
	/*
	Serial.println(red);
	Serial.println(green);
	Serial.println(blue);
	*/
	Driver.begin();
	Driver.SetColor(red, green, blue);
	Driver.end();
	
}

void Controller::powerOff(int sek) {
	delay(sek*1000);
	this->sendWireless(this->offCode);
}

int Controller::command(String s) {
	//Serial.println(s);
	int idx = s.indexOf('.');
	if (idx == -1) {return 0;}
	String cmd = "";
	String code = "";
  
	cmd = s.substring(0,idx);
  	code = s.substring(idx+1);
	
	if (cmd == "" or code == "") {
  	  return -1;
	}
  
	switch (cmd[0]) {
		case 'I':
	  		this->sendIR(code);
	  		break;
	  	
		case 'W':
	  		this->sendWireless(code);
	  		break;
	  	
		case 'C':
			this->rgbLed(code);
      		break;
	  	
		case 'T':
	  		this->getTemp(code.toInt());
	  		break;
			
		case 'L':
			this->getLight(code.toInt());
			break;
	}
      
  return 0;
}

void Controller::listen(bool echo) {
	while (Serial.available()) {
		char inC = Serial.read();
		
		if (inC == '\n') {
			if (echo) {
				Serial.println(this->inS);	
			}
			this->command(inS);
			this->inS = "";
			break;
		}
		this->inS += inC;
	}
	

}

