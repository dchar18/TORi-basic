/*****
 
 All the resources for this project:
 https://randomnerdtutorials.com/
 
*****/
// Loading the ESP8266WiFi library and the PubSubClient library
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const int ledGPIO5 = 5;
const int ledGPIO4 = 4;

const String ID = "esp8266_bed";
const char* device_ID = "esp8266_bed";

// TODO - replace "esp8266_bed/" with variable declared above
// done explicitly to avoid char/char*/String conversions and concatenations
const char* mode_off = "esp8266_bed/off";
const char* mode_random = "esp8266_bed/random";
const char* mode_christmas = "esp8266_bed/christmas";
const char* mode_study = "esp8266_bed/study";
const char* mode_party = "esp8266_bed/party";

// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "egon24";
const char* password = "4432egon";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.50.114";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

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

  // if all devices are supposed to respond to the change
  if(messageTemp == "all"){
    if(topic == "off"){
      Serial.println("All changing to \'off\'");
    }
    else if(topic == "random"){
      Serial.println("All changing to \'random\'");
    }
    else if(topic == "christmas"){
      Serial.println("All changing to \'christmas\'");
    }
    else if(topic == "study"){
      Serial.println("All changing to \'study\'");
    }
    else if(topic == "party"){
      Serial.println("All changing to \'party\'");
    }
  }
  // only the device with matching ID should respond
  else if(messageTemp.equals(ID)){
    if(topic == mode_off){
      Serial.println(ID + " changing to \'off\'");
    }
    else if(topic == mode_random){
      Serial.println(ID + " changing to \'random\'");
    }
    else if(topic == mode_christmas){
      Serial.println(ID + " changing to \'christmas\'");
    }
    else if(topic == mode_study){
      Serial.println(ID + " changing to \'study\'");
    }
    else if(topic == mode_party){
      Serial.println(ID + " changing to \'party\'");
    }
  }
  
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
     /*
     YOU  NEED TO CHANGE THIS NEXT LINE, IF YOU'RE HAVING PROBLEMS WITH MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, you will have to give a unique name to the ESP8266.
     Here's how it looks like now:
       if (client.connect("ESP8266Client")) {
     If you want more devices connected to the MQTT broker, you can do it like this:
       if (client.connect("ESPOffice")) {
     Then, for the other ESP:
       if (client.connect("ESPGarage")) {
      That should solve your MQTT multiple connections problem

     THE SECTION IN loop() function should match your device name
    */
    if (client.connect(device_ID)) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more LEDs in this example)
      client.subscribe(mode_off);
      client.subscribe(mode_random);
      client.subscribe(mode_christmas);
      client.subscribe(mode_study);
      client.subscribe(mode_party);
      client.subscribe("off");
      client.subscribe("random");
      client.subscribe("christmas");
      client.subscribe("study");
      client.subscribe("party");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// The setup function sets your ESP GPIOs to Outputs, starts the serial communication at a baud rate of 115200
// Sets your mqtt broker and sets the callback function
// The callback function is what receives messages and actually controls the LEDs
void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// For this project, you don't need to change anything in the loop function. 
// Basically it ensures that you ESP is connected to your broker
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
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
  
