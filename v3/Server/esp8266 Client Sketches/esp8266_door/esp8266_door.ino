/* Description: This sketch uses the esp8266 as a sensor that detects whether or not I am in the room.
 *              Whenever the ultrasonic distance sensor reads a distance around the difference between the
 *              sensor's height and the top of my head, it will trigger a signal to tunr off the other boards' leds
 */

 
// SETUP VARIABLES --------------------------------------------------------------------------------

// Loading the ESP8266WiFi library and the PubSubClient library
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

// Load in libraries for ultrasonic distance sensors
#include <NewPing.h>

// Server/Network Variables --------------------------------
const String ID = "esp8266_door";
const char* device_ID = "esp8266_door";

// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "egon24";
const char* password = "4432egon";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.50.115";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

HTTPClient http;

// Ultrasonic Distance Sensor Variables --------------------
#define INTERVAL 75 // determines how frequently the distance is checked
#define THRESHOLD 15 // determines how much the distance can vary by to trigger a change in state (in centimeters)
#define MAX_DISTANCE 250
#define ECHO_INNER    D1
#define TRIGGER_INNER D2
#define ECHO_OUTER    D5
#define TRIGGER_OUTER D6
#define FLAG    D0
#define PRESENT D3 // LOW when no one in room, HIGH when present
NewPing sensor_inner = NewPing(TRIGGER_INNER, ECHO_INNER, MAX_DISTANCE);
NewPing sensor_outer = NewPing(TRIGGER_OUTER, ECHO_OUTER, MAX_DISTANCE);

// device 0: esp8266_bed
// device 1: esp8266_desk
// device 2: esp8266_rclambo
const uint8_t num_devices = 3;
String devices[] = {"esp8266_bed", "esp8266_desk", "esp8266_rclambo"};
String prev_modes[] = {"off", "off", "rgb"};
int rgb_vals[num_devices][3] = {{0,0,0},{0,0,0},{0,0,0}};

// LED Strip variables ---------------------------
#define NUM_LEDS 6

// Loading led strip-related libraries
#define FASTLED_ESP8266_RAW_PIN_ORDER
#include <FastLED.h>
#define STRIP   D4

uint8_t BRIGHTNESS = 65;
#define VOLTS 5
#define MAX_MA 3000
CRGB leds[NUM_LEDS];
int _delay = 10;
int UPDATES_PER_SECOND = 400;

String led_mode = "off";
String prev_mode = "off";
int last_shift = 0; // used to decide when to continue fading
uint8_t curr_brightness = 65; // used for fading, BRIGHTNESS is max brightness
boolean dir = false; // true = increase brighness, false = decrease

// -----------------------------------------------

// these two flags are used to determine whether both sensors detected movement
// if only one flag is set to true, then don't react
//  - if FLAG_inner is true but FLAG_outer is false (or vice versa), then the door was closed/opened -> don't react
//  - if both are set to true, then someone passed by the door, so trigger a change in the present variable
boolean FLAG_inner = false;
boolean FLAG_outer = false;
boolean react = false; // true when FLAG_inner && FLAG_outer == true
boolean present = true;
boolean SENSOR_ON  = true; // used to determine whether the sensors should receive readings

#define TIMEOUT 200 // determines how long each FLAG_* will remain true before being reset
uint8_t distance_inner = -1; // store distance read using sensor inside the room
int time_activated_in = 0; // store the time at which the sensor was activated (if too much time passed since activation, reset FLAG_inner)
uint8_t distance_outer = -1;
int time_activated_out = 0;

int curr_time = 0;
int prev_time = 0;
int last_change = 0; // stores the last time a http request was made (limits how frequently a call is made)

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  FastLED.setMaxPowerInVoltsAndMilliamps(VOLTS, MAX_MA);
  FastLED.addLeds<WS2812, STRIP, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  
  pinMode(FLAG, OUTPUT);
  digitalWrite(FLAG, LOW);

  pinMode(PRESENT, OUTPUT);
  digitalWrite(PRESENT, LOW);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop()){
    client.connect(device_ID);
  }

  // deal with led strip 
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; /* motion speed */
  if(led_mode == "off"){
    // prevent a function call to off() if it remains off
    if(prev_mode != "off"){
      Serial.println("TURNING OFF");
      off();
      prev_mode = "off";
    }
  }
  else if(led_mode == "red_pulse"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "red_pulse";
    }
    pulse("red");
  }
  else if(led_mode == "green_pulse"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "green_pulse";
    }
    pulse("green");
  }
  else if(led_mode == "red_stable"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "red_stable";
    }
    stable("red");
  }
  else if(led_mode == "green_stable"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "green_stable";
    }
    stable("green");
  }

  // deal with sensors
  curr_time = millis();

  if(SENSOR_ON){
    // check distance
    distance_inner = sensor_inner.ping_cm();
    distance_outer = sensor_outer.ping_cm();

    // reset flags if timeout
    if(curr_time - time_activated_in >= TIMEOUT){
      FLAG_inner = false;
    }
    if(curr_time - time_activated_out >= TIMEOUT){
      FLAG_outer = false;
    }

    // update flags
    // use abs() in case distance_* is less than 38 (due to electrical errors)
    if(abs(distance_inner - 38) < THRESHOLD){
      FLAG_inner = true;
      time_activated_in = millis();
    }
    if(abs(distance_outer - 38) < THRESHOLD){
      FLAG_outer = true;
      time_activated_out = millis();
    }

//    Serial.print(distance_inner);
//    Serial.print(",");
//    Serial.println(distance_outer);
//
//    Serial.print("\t");
//    Serial.print(FLAG_inner);
//    Serial.print(",");
//    Serial.println(FLAG_outer);

    // check if both sensors were triggered
    if(FLAG_inner && FLAG_outer){
      react = true;
      // reset flags
      FLAG_outer = false;
      FLAG_inner = false;
    }
    else{
      react = false;
    }

    if(react){
      if(curr_time - last_change >= 1000){
//        Serial.println("< TRIGGERED >");
        last_change = millis();
        present = !present;
//        Serial.println("< FLIPPED >");

        // make HTTP request
        if(present){
//          Serial.println("\tON");
          digitalWrite(PRESENT, HIGH);

//          Serial.println("MAKING HTTP REQUEST");
          for(int i = 0; i < num_devices; i++){
            String url = "http://192.168.50.114:8181/" + devices[i] + "/" + prev_modes[i];
            if(prev_modes[i] == "rgb"){
              for(int j = 0; j < 3; j++){
                url = url + "/" + String(rgb_vals[i][j]);
              }
            }
//            Serial.println("\t" + url);
            http.begin(url);
            int httpCode = http.GET();
            http.end(); 
          } 
        } // end if(present)
        // present == false
        else{
//          Serial.println("\tOFF");
          digitalWrite(PRESENT, LOW);
          http.begin("http://192.168.50.114:8181/sync/off");
          int httpCode = http.GET();
          http.end(); 
        }
      }
    }
  }
  FastLED.show();
  FastLED.delay(1000 / UPDATES_PER_SECOND);
}

// HELPER FUNCTIONS -------------------------------------------------------------------------------
// connect ESP8266 to router
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

// This functions is executed when some device publishes a message to a topic that your ESP8266 is subscribed to
// Change the function below to add logic to your program, so when a device publishes a message to a topic that 
// your ESP8266 is subscribed you can actually do something
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  /* (topic, message) format options: 
   *  1 - (<board>/<mode>, <board>)
   *  2 - (<mode>, "all")
   *  3 - (<board>/rgb, <red>/<green>/<blue>)
   *  4 - (all/rgb, <red>/<green>/<blue>)
   *  5 - (esp8266_door, <option>)
   *  6 - (all/brightness, <brightness>)
   *  7 - (esp8266_door/brightness, <brightness>)
  */ 

  // option 6 & 7
  if(topic == "all/brightness" || topic == "esp8266_door/brightness"){
    Serial.println("CHANGING BRIGHTNESS");
    BRIGHTNESS = messageTemp.toInt();
    FastLED.setBrightness(BRIGHTNESS);
    Serial.print("Brightness: ");
    Serial.println(BRIGHTNESS);
  }
  // option 5
  else if(topic == "esp8266_door"){
//    if(messageTemp == "toggle"){
//      present = !present;
//    }
//    else if(messageTemp == "reset"){
//      present = true;
//      SENSOR_ON = true;
//    }
//    else{
//      if(messageTemp == "keep_on"){
//        present = true;
//      }
//      else if(messageTemp == "keep_off"){
//        present = false;
//      }
//      SENSOR_ON = false;
//    }
     Serial.println("MODE: " + messageTemp);
     led_mode = messageTemp;
  }
  else if(topic != "off"){
    Serial.println("\tUPDATING...");
    // option 2
    if(messageTemp.equals("all")){
      for(int i = 0; i < num_devices; i++){
        prev_modes[i] = topic;
      }
    }
    else{
      Serial.println("PARSING...");
      String topic_temp = topic;
      String device = topic_temp.substring(0,topic_temp.indexOf("/"));
      topic_temp = topic_temp.substring(topic_temp.indexOf("/")+1);
      String device_mode = topic_temp;
      
      if(device_mode == "rgb"){
        String temp = messageTemp;
        uint8_t red = temp.substring(0,temp.indexOf("/")).toInt();
        temp = temp.substring(temp.indexOf("/")+1);
    
        uint8_t green = temp.substring(0,temp.indexOf("/")).toInt();
        temp = temp.substring(temp.indexOf("/")+1);
    
        uint8_t blue = temp.toInt();

         // option 4
         if(device == "all"){
          // update every board's rgb values
          for(int i = 0; i < num_devices; i++){
            rgb_vals[i][0] = red;
            rgb_vals[i][1] = green;
            rgb_vals[i][2] = blue;
            prev_modes[i] = "rgb";
          }
         }
         // option 3
         else{
          int device_index = -1;
          for(int i = 0; i < num_devices; i++){
            if(device == devices[i]){
              device_index = i;
            }
          }
          // update target board's rgb values
          rgb_vals[device_index][0] = red;
          rgb_vals[device_index][1] = green;
          rgb_vals[device_index][2] = blue;
          prev_modes[device_index] = "rgb";
         }
      }
      // option 1
      else{
        // find the device's corresponding index
        int device_index = -1;
        for(int i = 0; i < num_devices; i++){
          if(device == devices[i]){
            device_index = i;
          }
        }
        // update the mode
        prev_modes[device_index] = device_mode;
      }
    }
  }
  for(int j = 0; j < num_devices-1; j++){
    Serial.print(prev_modes[j] + " - ");
  }
  Serial.println(prev_modes[num_devices-1]);
  
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(device_ID)) {
      digitalWrite(FLAG, LOW);
      Serial.println("connected");
      // Subscribe or resubscribe to a topic
      client.subscribe("#");
    } 
    else {
      /* Error codes:
       * -4 : MQTT_CONNECTION_TIMEOUT - the server didn't respond within the keepalive time
       * -3 : MQTT_CONNECTION_LOST - the network connection was broken
       * -2 : MQTT_CONNECT_FAILED - the network connection failed
       * -1 : MQTT_DISCONNECTED - the client is disconnected cleanly
       * 0 : MQTT_CONNECTED - the client is connected
       * 1 : MQTT_CONNECT_BAD_PROTOCOL - the server doesn't support the requested version of MQTT
       * 2 : MQTT_CONNECT_BAD_CLIENT_ID - the server rejected the client identifier
       * 3 : MQTT_CONNECT_UNAVAILABLE - the server was unable to accept the connection
       * 4 : MQTT_CONNECT_BAD_CREDENTIALS - the username/password were rejected
       * 5 : MQTT_CONNECT_UNAUTHORIZED - the client was not authorized to connect
       */
      digitalWrite(FLAG, HIGH);
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void off(){
  FastLED.clear();
}

void pulse(String color){
  curr_time = millis();
  if(curr_time - last_shift >= 100){
    last_shift = millis();
    stable(color);
    // increase brightness
    if(dir){
      if(curr_brightness < BRIGHTNESS){
        curr_brightness += 10;
        FastLED.setBrightness(curr_brightness);
      }
      else{
        dir = !dir;
      }
    }
    // decrease brightness
    else{
      if(curr_brightness >= 10){
        curr_brightness -= 10;
        FastLED.setBrightness(curr_brightness);
      }
      else{
        dir = !dir;
      }
    }
  }
}

void stable(String color){
  if(color == "red"){
    for( int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB(255,0,0);
    }
  }
  else{
    for( int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB(0,255,0);
    }
  }
}
