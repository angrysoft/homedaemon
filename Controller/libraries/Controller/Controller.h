#ifndef Controller_h
#define Controller_h
//Led strip Driver Pins
#define CLK 9//pins definitions for the driver        
#define DIO 10
//Light sensor
#define LIGHTPIN A0
//OneWire thermometr pin
#define ONE_WIRE_BUS 7
#define IROUTPIN 3
#define WIRELESS_TRANSMITER_PIN 11
#define WIRELESS_RECIVER_PIN 2

#include <IRremote.h>
#include <Arduino.h>
#include <RGBdriver.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <RCSwitch.h>


//#include <Wiring.h>

class Controller {
	public:
		Controller();
		//~Controller();
		void setupCtrl();
		
		void listen(bool echo);
	private:
		String inS;
		String offCode;
		IRrecv irrecv(int outPin);
		IRsend irsend;
		int sendIR(String code);
		int sendWireless(String code);
		int getTemp(int num);
		int getLight(int num);
		void rgbLed(String colors);
		void powerOff(int sek);
		int command(String s);
		int getCode(unsigned long receivedCode, unsigned int period);
};
#endif
