/* Description: This sketch is uploaded to each ESP8266 module to control a different set of LEDs
 *              After connecting to the specified WiFi network, the module creates a client and proceeds to connect 
 *              to the web server hosted by the raspberry pi using the specified IP address.
 *              Once connected, the client subscribes to topics that are sent from the server.
 *              Once an appropriate topic is published, the client reacts accordingly by 
 *              setting the led mode to be the one the user requested
 *              
 * Resources: https://randomnerdtutorials.com/raspberry-pi-publishing-mqtt-messages-to-esp8266/ (for communication)
 *            https://gist.github.com/kriegsman/756ea6dcae8e30845b5a (for twinkle modes
 */

// SETUP VARIABLES --------------------------------------------------------------------------------
// Loading the ESP8266WiFi library and the PubSubClient library
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// rc lambo variables ----------------------------------------------------------
const String ID = "esp8266_rclambo";
const char* device_ID = "esp8266_rclambo";

// done explicitly to avoid char/char*/String conversions and concatenations
const char* mode_off = "esp8266_rclambo/off";
const char* mode_rainbow = "esp8266_rclambo/rainbow";
const char* mode_rgb = "esp8266_rclambo/rgb";
int red = 0;
int green = 0;
int blue = 255;
int STATE = 0;

String mode = "";

// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "egon24";
const char* password = "4432egon";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.50.114";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

String led_mode = "rgb";
String prev_mode = "rgb";

int fade_time = 100;
int curr_time = 0;
int prev_time = 0;

const int right_red = D0;
const int right_green = D1;
const int right_blue = D2;

const int left_red = D3;
const int left_green = D4;
const int left_blue = D5;

const int FLAG = D6;

// --------------------------------------------------

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

  // only the device with matching ID should respond
  if(messageTemp.equals(ID)){
    // find what mode is being sent to the board
    if(topic == mode_off){
      Serial.println(ID + " changing to \'off\'");
      led_mode = "off";
    }
    else if(topic == mode_rainbow){
      Serial.println(ID + " changing to \'rainbow\'");
      led_mode = "rainbow";
    }
  }
  else if(messageTemp.equals("all")){
    led_mode = topic;
  }
  // message is "<red>/<green>/<blue>"
  // parse the RGB values
  else{
    String temp = messageTemp;
    red = temp.substring(0,temp.indexOf("/")).toInt();
    temp = temp.substring(temp.indexOf("/")+1);

    green = temp.substring(0,temp.indexOf("/")).toInt();
    temp = temp.substring(temp.indexOf("/")+1);

    blue = temp.toInt();
    
//    Serial.println(ID + " changing to " + red + "," + green + "," + blue);
    led_mode = "rgb";
  }
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
      client.subscribe(mode_off);
      client.subscribe(mode_rainbow);
      client.subscribe(mode_rgb);
      client.subscribe("off");
    } else {
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

// MAIN FUNCTIONS ---------------------------------------------------------------------------------
// The setup function sets your ESP GPIOs to Outputs, starts the serial communication at a baud rate of 115200
// Sets your mqtt broker and sets the callback function
// The callback function is what receives messages and actually controls the LEDs
void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  pinMode(left_red, OUTPUT);
  analogWrite(left_red, red);
  pinMode(left_green, OUTPUT);
  analogWrite(left_green, green);
  pinMode(left_blue, OUTPUT);
  analogWrite(left_blue, blue);

  pinMode(right_red, OUTPUT);
  analogWrite(right_red, red);
  pinMode(right_green, OUTPUT);
  analogWrite(right_green, green);
  pinMode(right_blue, OUTPUT);
  analogWrite(right_blue, blue);

  pinMode(FLAG, OUTPUT);
  digitalWrite(FLAG, LOW);
}

// For this project, you don't need to change anything in the loop function. 
// Basically it ensures that you ESP is connected to your broker
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

  // deal with leds
  if(led_mode == "off"){
    off();
    prev_mode = "off";
  }
  else if(led_mode == "rainbow"){
    // check the current mode is running its first iteration after off()
    if(prev_mode != "rainbow"){
      // reset values
      red = 0;
      green = 0;
      blue = 255;
      prev_mode = "rainbow";
    }
    curr_time = millis();
    if(curr_time - prev_time >= fade_time){
      prev_time = curr_time;
      rainbow();
    }
  }
  else if(led_mode == "rgb"){
    if(prev_mode == "off"){
      prev_mode = "rgb";
    }
    update_leds();
  }
}

// LED MODE FUNCTIONS -----------------------------------------------------------------------------
void off(){
  red = 0;
  green = 0;
  blue = 0;
  
  update_leds();
}

void rainbow(){
  if(STATE == 0){
    if(red == 255){
      STATE = 1;
    }
    else{
      red += 15;
      blue -= 15;
    }
  }
  else if(STATE == 1){
    if(green == 255){
      STATE = 2;
    }
    else{
      green += 15;
      red -= 15;
    }
  }
  // STATE == 2
  else{
    if(blue == 255){
      STATE = 0;
    }
    else{
      blue += 15;
      green -= 15;
    }
  }
  update_leds();
}

void update_leds(){
  analogWrite(left_red, red);
  analogWrite(right_red, red);

  analogWrite(left_green, green);
  analogWrite(right_green, green);

  analogWrite(left_blue, blue);
  analogWrite(right_blue, blue);
}
