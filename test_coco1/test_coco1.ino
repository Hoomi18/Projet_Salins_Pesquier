#include "heltec.h"
//#include "images.h"

#define BAND    868E6  //force configuration for LoRa 
#define txPower 14
#define frequency 868E6
#define spreadingFactor 7
#define signalBandwidth 125E3
#define codingRateDenominator 5
#define preambleLength 8
#define syncWord 0x34
String rssi = "RSSI --";
String packSize = "--";
String packet ;

//test variables :
long tem, hum;
unsigned int counter = 0;
int device_id = 713705, sensor_id=02; // ID of this End node

/*
void logo()
{
  Heltec.display->clear();
  Heltec.display->drawXbm(0, 5, logo_width, logo_height, logo_bits);
  Heltec.display->display();
}*/

void setup()
{
  //WIFI Kit series V1 not support Vext control
  Heltec.begin(true /*DisplayEnable Enable*/, true /*Heltec.Heltec.Heltec.LoRa Disable*/, true /*Serial
  Enable*/, true /*PABOOST Enable*/, BAND /*long BAND*/);
  Heltec.display->init();
  Heltec.display->flipScreenVertically();
  Heltec.display->setFont(ArialMT_Plain_10);
  //logo();
  delay(1500);
  Heltec.display->clear();
  Heltec.display->drawString(0, 0, "Heltec.LoRa Initial success!");
  Heltec.display->display();
  delay(1000);

  // Force LoRa configuration
  LoRa.setFrequency(frequency);
  LoRa.setSpreadingFactor(spreadingFactor);
  LoRa.setSignalBandwidth(signalBandwidth);
  LoRa.setCodingRate4(codingRateDenominator);
  LoRa.setPreambleLength(preambleLength);
  LoRa.setSyncWord(syncWord);
  delay(1000);
}

void loop()
{
  Heltec.display->clear();
  Heltec.display->setTextAlignment(TEXT_ALIGN_LEFT);
  Heltec.display->setFont(ArialMT_Plain_10);

  //generate variables for test
  tem = random(15, 22);  // Generate a random temperature.
  hum = random(30, 50);  // Generate a random humidity.

  Heltec.display->drawString(0, 0, "Sending temp : ");
  Heltec.display->drawString(90, 0, String(tem));
  Heltec.display->drawString(0, 10, "Sending hum : ");
  Heltec.display->drawString(90, 10, String(hum));
  Heltec.display->drawString(0, 20, "Counter : ");
  Heltec.display->drawString(90, 20, String(counter));
  Heltec.display->display();

  // send packet
  LoRa.beginPacket();
  LoRa.setTxPower(14, RF_PACONFIG_PASELECT_PABOOST);
  LoRa.beginPacket();
  LoRa.print("<");
  LoRa.print(device_id);
  LoRa.print(">temperature=");
  LoRa.print(tem);
  LoRa.print("&humidity=");
  LoRa.print(hum);
  LoRa.print("&sensor_id=");
  LoRa.print(sensor_id);
  LoRa.endPacket();

  counter++;
  digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
  delay(4000);
}
