#include <string.h>
#include "DFRobot_SHT20.h"
#include <stdlib.h>

String HS_Send = "1";
String data_string;
DFRobot_SHT20 sht20(&Wire, SHT20_I2C_ADDR);

#define PMS7003_PREAMBLE_1  0x42 // From PMS7003 datasheet
#define PMS7003_PREAMBLE_2  0x4D
#define PMS7003_DATA_LENGTH 31
String Humid, Temp, _pm1, _pm25, _pm10, CO;

int sensorPin = A0;
unsigned long time;

void setup()
{
  Serial.begin(115200);
  Serial1.begin(9600); 
  Serial3.begin(115200);

  // Init SHT20 Sensor
  sht20.initSHT20();
  delay(100);
  Serial.println("Sensor init finish!");
  sht20.checkSHT20();
}

void readSensor() {
  float num1 = rand() % 1850 + 150;
  float num2 = rand() % 1850 + 150;
  float num3 = rand() % 1850 + 150;
  // float num1 = rand() % 50;
  // float num2 = rand() % 50;
  // float num3 = rand() % 50;
  float num4 = rand() % 40;
   _pm1 = String(num1, 1);
   _pm25 = String(num2, 1);
   _pm10 = String(num3, 1);
   CO = String(num4, 1);
}

void readsht20() { 
  //--------------Temp and Humid----------------------------------------------------  
  float humid = sht20.readHumidity();
  float  temp = sht20.readTemperature();
  
  Humid = String(humid,1);// không có số thập phân
  Temp = String(temp,1);// có 1 số thập phân
}

void readco() { 
  CO = analogRead(sensorPin);
  delay(100);
}

void loop()
{ 
if ( (unsigned long) (millis() - time) > 5000){
  readSensor();
  readsht20();
  // readco();
  
  data_string = "";
/*
//--------------Temp and Humid----------------------------------------------------  
  float humid = sht20.readHumidity();
  float  temp = sht20.readTemperature();
  
  Humid = String(humid,1);// không có số thập phân
  Temp = String(temp,1);// có 1 số thập phân
//-----------------------CO sensor------------------------------------------------
  CO = analogRead(sensorPin);
  delay(100);
  */
//-----------------------------------------------------------------------------------------
  data_string = HS_Send + "-" + Temp + "-" + Humid + "-" + _pm1 + "-" + _pm25 + "-" + _pm10 + "-" + CO;
  Serial.println(data_string);
  Serial3.println(data_string);// gửi dữ liệu lên gateway qua cổng uart 3 LoRa
  //delay(100);
  time = millis();
  }
}