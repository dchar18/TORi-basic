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

// For each board, change the values of the following variables:
// - NUM_LEDS
// - ID
// - device_ID
// - all the modes

// SETUP VARIABLES --------------------------------------------------------------------------------
// Loading the ESP8266WiFi library and the PubSubClient library
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// desk variables ----------------------------------------------------------
const String ID = "esp8266_desk";
const char* device_ID = "esp8266_desk";

#define NUM_LEDS 270 // used for esp8266_desk

// TODO - replace "esp8266_bed/" with variable declared above
// done explicitly to avoid char/char*/String conversions and concatenations
const char* mode_off = "esp8266_desk/off";
const char* mode_random = "esp8266_desk/random";
const char* mode_christmas = "esp8266_desk/christmas";
const char* mode_study = "esp8266_desk/study";
const char* mode_party = "esp8266_desk/party";
const char* mode_twinkle_christmas = "esp8266_desk/twinkle_christmas";
const char* mode_twinkle_blue = "esp8266_desk/twinkle_blue";
const char* mode_twinkle_green = "esp8266_desk/twinkle_green";
const char* mode_snow = "esp8266_desk/snow";

// bed variables -----------------------------------------------------------
//const String ID = "esp8266_bed";
//const char* device_ID = "esp8266_bed";
//
//#define NUM_LEDS 110 // used for esp8266_bed
//
//const char* mode_off = "esp8266_bed/off";
//const char* mode_random = "esp8266_bed/random";
//const char* mode_christmas = "esp8266_bed/christmas";
//const char* mode_study = "esp8266_bed/study";
//const char* mode_party = "esp8266_bed/party";
//const char* mode_twinkle_christmas = "esp8266_bed/twinkle_christmas";
//const char* mode_twinkle_blue = "esp8266_bed/twinkle_blue";
//const char* mode_twinkle_green = "esp8266_bed/twinkle_green";
//const char* mode_snow = "esp8266_bed/snow";

// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "egon24";
const char* password = "4432egon";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.50.114";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

// Loading led strip-related libraries
#define FASTLED_ESP8266_RAW_PIN_ORDER
#include <FastLED.h>

const int LED_PIN = D4;
const int FLAG_LED = D5;
#define BRIGHTNESS 64
#define VOLTS 5
#define MAX_MA 3000
CRGB leds[NUM_LEDS];
int count = 0;
int _delay = 10;
int UPDATES_PER_SECOND = 400;
int NUM_COLOR_MODES = 5;
String modes[] = {"christmas", "study", "party", "twinkle_christmas", "twinkle_blue", "twinkle_green", "snow"};

// used for the "twinkle" modes ---------------------
// Overall twinkle speed.
// 0 (VERY slow) to 8 (VERY fast).  
// 4, 5, and 6 are recommended, default is 4.
#define TWINKLE_SPEED 4

// Overall twinkle density.
// 0 (NONE lit) to 8 (ALL lit at once).  
// Default is 5.
#define TWINKLE_DENSITY 6

// Background color for 'unlit' pixels
CRGB gBackgroundColor = CRGB::Black; 

// If AUTO_SELECT_BACKGROUND_COLOR is set to 1,
// then for any palette where the first two entries 
// are the same, a dimmed version of that color will
// automatically be used as the background color.
#define AUTO_SELECT_BACKGROUND_COLOR 0

// If COOL_LIKE_INCANDESCENT is set to 1, colors will 
// fade out slighted 'reddened', similar to how
// incandescent bulbs change color as they get dim down.
#define COOL_LIKE_INCANDESCENT 1

CRGBPalette16 targetPalette;
// --------------------------------------------------


CRGBPalette16 currentPalette;
TBlendType    currentBlending;
String led_mode = "off";
String prev_mode = "off";

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

  // if all devices are supposed to respond to the change
  if(messageTemp == "all"){
    if(topic == "off"){
      Serial.println("All changing to \'off\'");
      led_mode = "off";
    }
    else if(topic == "random"){
      Serial.println("All changing to \'random\'");
      led_mode = "random";
    }
    else if(topic == "christmas"){
      Serial.println("All changing to \'christmas\'");
      led_mode = "christmas";
      // UPDATES_PER_SECOND = 250;
    }
    else if(topic == "study"){
      Serial.println("All changing to \'study\'");
      led_mode = "study";
      // UPDATES_PER_SECOND = 200;
    }
    else if(topic == "party"){
      Serial.println("All changing to \'party\'");
      led_mode = "party";
      // UPDATES_PER_SECOND = 400;
    }
    else if(topic == "twinkle_christmas"){
      Serial.println("All changing to \'twinkle_christmas\'");
      led_mode = "twinkle_christmas";
      // UPDATES_PER_SECOND = 400;
    }
    else if(topic == "twinkle_blue"){
      Serial.println("All changing to \'twinkle_blue\'");
      led_mode = "twinkle_blue";
      // UPDATES_PER_SECOND = 400;
    }
    else if(topic == "twinkle_green"){
      Serial.println("All changing to \'twinkle_green\'");
      led_mode = "twinkle_green";
      // UPDATES_PER_SECOND = 400;
    }
    else if(topic == "snow"){
      Serial.println("All changing to \'snow\'");
      led_mode = "snow";
      // UPDATES_PER_SECOND = 400;
    }
  }
  // only the device with matching ID should respond
  else if(messageTemp.equals(ID)){
    if(topic == mode_off){
      Serial.println(ID + " changing to \'off\'");
      led_mode = "off";
    }
    else if(topic == mode_random){
      Serial.println(ID + " changing to \'random\'");
      led_mode = "random";
    }
    else if(topic == mode_christmas){
      Serial.println(ID + " changing to \'christmas\'");
      led_mode = "christmas";
      // UPDATES_PER_SECOND = 400;
    }
    else if(topic == mode_study){
      Serial.println(ID + " changing to \'study\'");
      led_mode = "study";
      // UPDATES_PER_SECOND = 200;
    }
    else if(topic == mode_party){
      Serial.println(ID + " changing to \'party\'");
      led_mode = "party";
      // UPDATES_PER_SECOND = 500;
    }
    else if(topic == mode_twinkle_christmas){
      Serial.println(ID + " changing to \'twinkle_christmas\'");
      led_mode = "twinkle_christmas";
    }
    else if(topic == mode_twinkle_blue){
      Serial.println(ID + " changing to \'twinkle_blue\'");
      led_mode = "twinkle_blue";
    }
    else if(topic == mode_twinkle_green){
      Serial.println(ID + " changing to \'twinkle_green\'");
      led_mode = "twinkle_green";
    }
    else if(topic == mode_snow){
      Serial.println(ID + " changing to \'snow\'");
      led_mode = "snow";
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
      digitalWrite(FLAG_LED, LOW);
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      client.subscribe(mode_off);
      client.subscribe(mode_random);
      client.subscribe(mode_christmas);
      client.subscribe(mode_study);
      client.subscribe(mode_party);
      client.subscribe(mode_twinkle_christmas);
      client.subscribe(mode_twinkle_blue);
      client.subscribe(mode_twinkle_green);
      client.subscribe(mode_snow);
      client.subscribe("off");
      client.subscribe("random");
      client.subscribe("christmas");
      client.subscribe("study");
      client.subscribe("party");
      client.subscribe("twinkle_christmas");
      client.subscribe("twinkle_blue");
      client.subscribe("twinkle_green");
      client.subscribe("snow");
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
      digitalWrite(FLAG_LED, HIGH);
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

  FastLED.setMaxPowerInVoltsAndMilliamps(VOLTS, MAX_MA);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  currentPalette = RainbowColors_p;
  currentBlending = LINEARBLEND;

  pinMode(FLAG_LED, OUTPUT);
  digitalWrite(FLAG_LED, LOW);
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

  // deal with led strip 
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; /* motion speed */
  if(led_mode == "off"){
    // prevent a function call to off() if it remains off
    if(prev_mode != "off"){
      off();
      prev_mode = "off";
    }
  }
  else if(led_mode == "random"){
    // check the current mode is running its first iteration after off()
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "random";
    }
    random_mode(startIndex);
  }
  else if(led_mode == "christmas"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "christmas";
    }
    currentPalette = ChristmasColors_p;
    use_palette(startIndex);
  }
  else if(led_mode == "study"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "study";
    }
    currentPalette = StudyColors_p;
    use_palette(startIndex);
  }
  else if(led_mode == "party"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "party";
    }
    currentPalette = RainbowColors_p;
    use_palette(startIndex);
  }
  else if(led_mode == "twinkle_christmas"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "twinkle_christmas";
    }
    currentPalette = RedGreenWhite_p;
    twinkle();
  }
  else if(led_mode == "twinkle_blue"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "twinkle_blue";
    }
    currentPalette = Ice_p;
    twinkle();
  }
  else if(led_mode == "twinkle_green"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "twinkle_green";
    }
    currentPalette = Holly_p;
    twinkle();
  }
  else if(led_mode == "snow"){
    if(prev_mode == "off"){
      startIndex = 0;
      prev_mode = "snow";
    }
    currentPalette = Snow_p;
    twinkle();
  }
  FastLED.show();
  FastLED.delay(1000 / UPDATES_PER_SECOND);
  
}

// LED MODE FUNCTIONS -----------------------------------------------------------------------------
void off(){
  FastLED.clear();
}

void random_mode(uint8_t colorIndex){
  uint8_t rand_num = random(NUM_COLOR_MODES);
  led_mode = modes[rand_num];
  if(rand_num < 3){
    use_palette(colorIndex);
  }
  else{
    // christmas twinkle
    if(rand_num == 3){
      currentPalette = RedGreenWhite_p;
    }
    // twinkle blue
    else if(rand_num == 4){
      currentPalette = Ice_p;
    }
    // twinkle green
    else if(rand_num == 5){
      currentPalette = Holly_p;
    }
    // twinkle snow
    else if(rand_num == 6){
      currentPalette = Snow_p;
    }
    twinkle();
  }
}

void use_palette(uint8_t colorIndex){
  uint8_t brightness = 255;
  for( int i = 0; i < NUM_LEDS; i++) {
      leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
      colorIndex += 3;
  }
  FastLED.show();
  FastLED.delay(1000 / UPDATES_PER_SECOND);
}

void twinkle(){
  // "PRNG16" is the pseudorandom number generator
  // It MUST be reset to the same starting value each time
  // this function is called, so that the sequence of 'random'
  // numbers that it generates is (paradoxically) stable.
  uint16_t PRNG16 = 11337;
  
  uint32_t clock32 = millis();

  // Set up the background color, "bg".
  // if AUTO_SELECT_BACKGROUND_COLOR == 1, and the first two colors of
  // the current palette are identical, then a deeply faded version of
  // that color is used for the background color
  CRGB bg;
  if( (AUTO_SELECT_BACKGROUND_COLOR == 1) && (currentPalette[0] == currentPalette[1] )){
    bg = currentPalette[0];
    uint8_t bglight = bg.getAverageLight();
    if( bglight > 64) {
      bg.nscale8_video( 16); // very bright, so scale to 1/16th
    } else if( bglight > 16) {
      bg.nscale8_video( 64); // not that bright, so scale to 1/4th
    } else {
      bg.nscale8_video( 86); // dim, scale to 1/3rd.
    }
  } 
  else {
    bg = gBackgroundColor; // just use the explicitly defined background color
  }

  uint8_t backgroundBrightness = bg.getAverageLight();

  for( CRGB& pixel: leds) {
    PRNG16 = (uint16_t)(PRNG16 * 2053) + 1384; // next 'random' number
    uint16_t myclockoffset16= PRNG16; // use that number as clock offset
    PRNG16 = (uint16_t)(PRNG16 * 2053) + 1384; // next 'random' number
    // use that number as clock speed adjustment factor (in 8ths, from 8/8ths to 23/8ths)
    uint8_t myspeedmultiplierQ5_3 =  ((((PRNG16 & 0xFF)>>4) + (PRNG16 & 0x0F)) & 0x0F) + 0x08;
    uint32_t myclock30 = (uint32_t)((clock32 * myspeedmultiplierQ5_3) >> 3) + myclockoffset16;
    uint8_t  myunique8 = PRNG16 >> 8; // get 'salt' value for this pixel

    // We now have the adjusted 'clock' for this pixel, now we call
    // the function that computes what color the pixel should be based
    // on the "brightness = f( time )" idea.
    CRGB c = computeOneTwinkle( myclock30, myunique8);

    uint8_t cbright = c.getAverageLight();
    int16_t deltabright = cbright - backgroundBrightness;
    if( deltabright >= 32 || (!bg)) {
      // If the new pixel is significantly brighter than the background color, 
      // use the new color.
      pixel = c;
    } else if( deltabright > 0 ) {
      // If the new pixel is just slightly brighter than the background color,
      // mix a blend of the new color and the background color
      pixel = blend( bg, c, deltabright * 8);
    } else { 
      // if the new pixel is not at all brighter than the background color,
      // just use the background color.
      pixel = bg;
    }
  }
}

//  This function takes a time in pseudo-milliseconds,
//  figures out brightness = f( time ), and also hue = f( time )
//  The 'low digits' of the millisecond time are used as 
//  input to the brightness wave function.  
//  The 'high digits' are used to select a color, so that the color
//  does not change over the course of the fade-in, fade-out
//  of one cycle of the brightness wave function.
//  The 'high digits' are also used to determine whether this pixel
//  should light at all during this cycle, based on the TWINKLE_DENSITY.
CRGB computeOneTwinkle( uint32_t ms, uint8_t salt) {
  uint16_t ticks = ms >> (8-TWINKLE_SPEED);
  uint8_t fastcycle8 = ticks;
  uint16_t slowcycle16 = (ticks >> 8) + salt;
  slowcycle16 += sin8( slowcycle16);
  slowcycle16 =  (slowcycle16 * 2053) + 1384;
  uint8_t slowcycle8 = (slowcycle16 & 0xFF) + (slowcycle16 >> 8);
  
  uint8_t bright = 0;
  if( ((slowcycle8 & 0x0E)/2) < TWINKLE_DENSITY) {
    bright = attackDecayWave8( fastcycle8);
  }

  uint8_t hue = slowcycle8 - salt;
  CRGB c;
  if( bright > 0) {
    c = ColorFromPalette( currentPalette, hue, bright, NOBLEND);
    if( COOL_LIKE_INCANDESCENT == 1 ) {
      coolLikeIncandescent( c, fastcycle8);
    }
  } 
  else {
    c = CRGB::Black;
  }
  return c;
}

// This function is like 'triwave8', which produces a 
// symmetrical up-and-down triangle sawtooth waveform, except that this
// function produces a triangle wave with a faster attack and a slower decay:
//
//     / \ 
//    /     \ 
//   /         \ 
//  /             \ 
//

uint8_t attackDecayWave8( uint8_t i)
{
  if( i < 86) {
    return i * 3;
  } else {
    i -= 86;
    return 255 - (i + (i/2));
  }
}

// This function takes a pixel, and if its in the 'fading down'
// part of the cycle, it adjusts the color a little bit like the 
// way that incandescent bulbs fade toward 'red' as they dim.
void coolLikeIncandescent( CRGB& c, uint8_t phase)
{
  if( phase < 128) return;

  uint8_t cooling = (phase - 128) >> 4;
  c.g = qsub8( c.g, cooling);
  c.b = qsub8( c.b, cooling * 2);
}
