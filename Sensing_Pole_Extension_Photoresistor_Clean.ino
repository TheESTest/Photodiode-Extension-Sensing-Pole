/* DIY EMT Conduit Telescoping Pole - Photoresistor Extension Sensing
 * 
 * The utilized library Adafruit_ADS1X15 is copyrighted by Adafruit Industries
 * and is licensed under the MIT License.
 * 
 */

#include <Wire.h>
#include <Adafruit_ADS1X15.h>

const int numReadings0 = 20;
float readings0[numReadings0];
int readIndex0 = 0;
float total0 = 0;
float average0 = 0;

const int numReadings1 = 20;
float readings1[numReadings1];
int readIndex1 = 0;
float total1 = 0;
float average1 = 0;

int val0;
int val1;

Adafruit_ADS1115 ads1115; // Construct an ads1115 object

void setup(void)
{
  Serial.begin(9600);
  ads1115.begin();  // Initialize ads1015 at the default address 0x48
}

void loop(void)
{
  int16_t adc0, adc1;

  //Read photoresistor voltage divider #1
  total0 = total0 - readings0[readIndex0];
  readings0[readIndex0] = ads1115.readADC_SingleEnded(0);
  total0 = total0 + readings0[readIndex0];
  readIndex0 = readIndex0 + 1;
  if (readIndex0 >= numReadings0) {
    readIndex0 = 0;
  }
  average0 = float(total0) / float(numReadings0);

  //Read photoresistor voltage divider #2
  total1 = total1 - readings1[readIndex1];
  readings1[readIndex1] = ads1115.readADC_SingleEnded(1);
  total1 = total1 + readings1[readIndex1];
  readIndex1 = readIndex1 + 1;
  if (readIndex1 >= numReadings1) {
    readIndex1 = 0;
  }
  average1 = float(total1) / float(numReadings1);

  //Print out the two rolling average values for photoresistors #1 and #2
  Serial.println(String(average0) + "," + String(average1));

}
