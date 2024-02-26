#include "Arduino.h"
#include <SoftwareSerial.h>
#include <Adafruit_AHT10.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

Adafruit_BMP280 bmp;
Adafruit_AHT10 aht;

const byte rxPin = 9;
const byte txPin = 8;
SoftwareSerial BTSerial(rxPin, txPin); // RX TX
int moisture_signal = A0;

int max_moist = 800;
int min_moist = 500;
void setup() {
// define pin modes for tx, rx:
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  BTSerial.begin(9600);
  Serial.begin(9600);
  
  while ( !Serial ) {delay(100);}

  if (!bmp.begin()){
    Serial.println("Could not find BPM280? Check wiring");
    while (1) delay(10);
  }
  if (! aht.begin()) {
    Serial.println("Could not find AHT10? Check wiring");
    while (1) delay(10);
  }
  
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
                
  Serial.println("AHT10 found");
  Serial.println("BPM280 found");
  Serial.println("Test");
}


String message = "";

void loop() {
  sensors_event_t humidity, temp;

  while (BTSerial.available() > 0) {
    char data = (char) BTSerial.read();
      if (data == ';'){
        int Moisture = analogRead(moisture_signal);
        Serial.println("begin"); 
        
        aht.getEvent(&humidity, &temp);// populate temp and humidity objects with fresh data
        
        //Serial.print("Temperature: "); Serial.print(temp.temperature); Serial.println(" degrees C");
        //Serial.print("Humidity: "); Serial.print(humidity.relative_humidity); Serial.println("% rH");
        
        //Serial.println(Moisture); 

        BTSerial.println("Plant Data: "); 
        BTSerial.print("Moisture: ");
        BTSerial.println(Moisture);

        BTSerial.print("Tempreture: ");
        BTSerial.println(temp.temperature);

        BTSerial.print("Humidity: ");
        BTSerial.println(humidity.relative_humidity);

        BTSerial.print(F("Pressure: "));
        BTSerial.println(bmp.readPressure());
      }
      else if (data == '%'){
          max_moist = 0;
          min_moist = 0;
          int count = 0;
          delay(100);
           while (BTSerial.available() > 0) {
             char d = (char) BTSerial.read();
             
             if (count <= 3){
                min_moist *= 10;
                min_moist += (d-48);
             }
             if (count > 3 && count <= 7){
              max_moist *= 10;
              max_moist += (d-48);
             }
             if (count >= 8){
                break;
              }
              count++;
           }
           Serial.println(min_moist);
           Serial.println(max_moist);
      }
      else {
        continue;
      }
  }
}