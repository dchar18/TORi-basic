#define FASTLED_ESP8266_RAW_PIN_ORDER
#include <FastLED.h>
#include <ESP8266WiFi.h>

const int LED_PIN = D4;
const int FLAG_LED = D5;
#define NUM_LEDS 270
#define BRIGHTNESS  64
CRGB leds[NUM_LEDS];
int count = 0;
int _delay = 10;
#define UPDATES_PER_SECOND 200

CRGBPalette16 currentPalette;
TBlendType    currentBlending;

// store name and password for the access point
const char* ssid = "esp8266LED";
const char* password = "ledesp8266";

boolean flag = false;

void setup() {
//  Serial.begin(115200);
//  delay(10);
//  Serial.println('\n');

  // start the access point so that other devices can connect to it
//  boolean result = WiFi.softAP(ssid, password);
//  if(result == true)
//  {
//    Serial.println("Ready");
//    Serial.print("Access Point \"");
//    Serial.print(ssid);
//    Serial.println("\" started");
//
//    Serial.print("IP address:\t");
//    Serial.println(WiFi.softAPIP());
//  }
//  else
//  {
//    Serial.println("Failed!");
//  }
  
  // put your setup code here, to run once:
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  currentPalette = RainbowColors_p;
//  currentBlending = LINEARBLEND;

//  currentPalette = ChristmasColors_p;
  currentBlending = LINEARBLEND;

  pinMode(FLAG_LED, OUTPUT);
  digitalWrite(FLAG_LED, LOW);
  
//  startup();
}

void loop() {
  // put your main code here, to run repeatedly:
//  if(WiFi.softAPgetStationNum() > 0){
//    digitalWrite(FLAG_LED, HIGH);
////    Serial.println("Someone connected!");
//  }
//  else{
//    digitalWrite(FLAG_LED, LOW);
////    Serial.println("0 connections");
//  }

//  if(count == 0){
//    leds[0] = CRGB(0,255,0);
//    for(int j = 1; j < NUM_LEDS-1; j++){
//      leds[j] = CRGB(0,255,0);
//      leds[j+1] = CRGB(0,255,0);
//      leds[j-1] = CRGB(255,0,0);
//      FastLED.show();
//      delay(_delay);
//    }
//    count = 1;
//  }
//  else if(count == 1){
//    leds[0] = CRGB(255,0,0);
//    for(int j = 1; j < NUM_LEDS-1; j++){
//        leds[j] = CRGB(255,0,0);
//        leds[j+1] = CRGB(255,0,0);
//        leds[j-1] = CRGB(0,255,0);
//        FastLED.show();
//        delay(_delay);
//    }
////    FastLED.show();
////    delay(_delay);
//    count = 0;
//  }

  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; /* motion speed */
  rainbow(startIndex);
  FastLED.show();
  FastLED.delay(1000 / UPDATES_PER_SECOND);
}

void startup(){
  FastLED.clear();
  int _delay = 100;
  leds[0] = CRGB(255,0,0);
  FastLED.show();
  delay(_delay);
  for(int i = 1; i < NUM_LEDS; i++){
    leds[i] = CRGB(255,0,0);
    leds[i-1] = CRGB::Black;
    FastLED.show();
    delay(_delay);
  }
  leds[NUM_LEDS] = CRGB::Black;
  FastLED.show();
  delay(_delay);
  for(int i = NUM_LEDS-1; i >= 0; i--){
    leds[i] = CRGB(0,255,0);
    leds[i+1] = CRGB::Black;
    FastLED.show();
    delay(_delay);
  }
  leds[0] = CRGB::Black;
  FastLED.show();
  delay(_delay);
}

void rainbow(uint8_t colorIndex){
  uint8_t brightness = 255;
  for( int i = 0; i < NUM_LEDS; i++) {
      leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
      colorIndex += 3;
  }
  FastLED.show();
  FastLED.delay(1000 / UPDATES_PER_SECOND);
}


void Christmas(){
  
}
