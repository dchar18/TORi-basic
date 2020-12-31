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
const char* mqtt_server = "192.168.50.114";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

HTTPClient http;

// Ultrasonic Distance Sensor Variables --------------------
#define INTERVAL 100 // determines how frequently the distance is checked
#define THRESHOLD 10 // determines how much the distance can vary by to trigger a change in state (in centimeters)
#define MAX_DISTANCE 250
#define ECHO    D1
#define TRIGGER D2
#define FLAG    D0
#define PRESENT D4 // LOW when no one in room, HIGH when present
NewPing sensor = NewPing(TRIGGER, ECHO, MAX_DISTANCE);

// device 0: esp8266_bed
// device 1: esp8266_desk
// device 2: esp8266_rclambo
uint8_t num_devices = 3;
String devices[] = {"esp8266_bed", "esp8266_desk", "esp8266_rclambo"};
String prev_modes[] = {"off", "off", "rgb"};
int rgb_vals[] = {0,0,255};

boolean present = true;
uint8_t distance = -1;
int prev_time = 0;
int curr_time = 0;
int last_change = 0;
//int total = 0;
//double avg = 0; // keeps track of the average over 10 readings to prevent alternation when something is constantly in front of the sensor

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // .connect(HOST_NAME, HTTP_PORT)
//  if(http_client.connect("192.168.50.114", )){
//    Serial.println("Connected to server");
//  }

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
     /*
     YOU  NEED TO CHANGE THIS NEXT LINE, IF YOU'RE HAVING PROBLEMS WITH MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, you will have to give a unique name to the ESP8266.
     Here's how it looks like now:
       client.connect("ESP8266Client");
     If you want more devices connected to the MQTT broker, you can do it like this:
       client.connect("ESPOffice");
     Then, for the other ESP:
       client.connect("ESPGarage");
      That should solve your MQTT multiple connections problem

     THE SECTION IN recionnect() function should match your device name
    */
    client.connect(device_ID);
  }

  curr_time = millis();
  if(curr_time - prev_time >= INTERVAL){
    prev_time = curr_time;
    // check distance
    distance = sensor.ping_cm();
//    total += distance;

    Serial.println(distance);
    if(distance > 15){
      if(distance - 38 < THRESHOLD){
        if(curr_time - last_change >= 1000){
          last_change = curr_time;
          present = !present;

          Serial.println("MAKING HTTP REQUEST");
          if(present){
            Serial.println("\tON");
            digitalWrite(PRESENT, HIGH);

            for(int i = 0; i < num_devices; i++){
              String url = "http://192.168.50.114:8181/" + devices[i] + "/" + prev_modes[i];
              if(prev_modes[i] == "rgb"){
                for(int j = 0; j < 3; j++){
                  url = url + "/" + String(rgb_vals[j]);
                }
              }
              Serial.println("\t" + url);
              http.begin(url);
              int httpCode = http.GET();
              http.end(); 
            }
            
          }
          else{
            Serial.println("\tOFF");
            digitalWrite(PRESENT, LOW);
            http.begin("http://192.168.50.114:8181/off/sync");
            int httpCode = http.GET();
            http.end(); 
          }
          
//          int httpCode = http.GET();            //Send the request
//          String payload = http.getString();
//          Serial.println("\tCode: " + httpCode);   //Print HTTP return code
//          http.end(); 
        }
      }
    }
  }
  
  
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
   *  3 - (<board>/rbg, <red>/<green>/<blue>)
  */ 

  if(topic != "off"){
    Serial.println("\tUPDATING...");
    // option 2
    if(messageTemp.equals("all")){
      for(int i = 0; i < num_devices; i++){
        prev_modes[i] = topic;
      }
    }
    else{
      String topic_temp = topic;
      String device = topic_temp.substring(0,topic_temp.indexOf("/"));
      topic_temp = topic_temp.substring(topic_temp.indexOf("/")+1);
      String device_mode = topic_temp;
      
      // option 3
      if(device_mode == "rgb"){
        String temp = messageTemp;
        rgb_vals[0] = temp.substring(0,temp.indexOf("/")).toInt();
        temp = temp.substring(temp.indexOf("/")+1);
    
        rgb_vals[1] = temp.substring(0,temp.indexOf("/")).toInt();
        temp = temp.substring(temp.indexOf("/")+1);
    
        rgb_vals[2] = temp.toInt(); 
      }
      // option 1
      else{
        if(device == "esp8266_bed"){
          prev_modes[0] = device_mode;
        }
        else if(device == "esp8266_desk"){
          prev_modes[1] = device_mode;
        }
        else if(device == "esp8266_rclambo"){
          prev_modes[2] = device_mode;
        }
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
