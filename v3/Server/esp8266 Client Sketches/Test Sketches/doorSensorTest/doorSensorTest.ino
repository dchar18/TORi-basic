#include <NewPing.h>

// Ultrasonic Distance Sensor Variables --------------------
#define INTERVAL 50 // determines how frequently the distance is checked
#define THRESHOLD 10 // determines how much the distance can vary by to trigger a change in state (in centimeters)
#define MAX_DISTANCE 250
#define ECHO_INNER    D1
#define TRIGGER_INNER D2
#define ECHO_OUTER    D5
#define TRIGGER_OUTER D6
#define FLAG    D0
#define PRESENT D4 // LOW when no one in room, HIGH when present
NewPing sensor_inner = NewPing(TRIGGER_INNER, ECHO_INNER, MAX_DISTANCE);
NewPing sensor_outer = NewPing(TRIGGER_OUTER, ECHO_OUTER, MAX_DISTANCE);

// these two flags are used to determine whether both sensors detected movement
// if only one flag is set to true, then don't react
//  - if FLAG_inner is true but FLAG_outer is false (or vice versa), then the door was closed/opened -> don't react
//  - if both are set to true, then someone passed by the door, so trigger a change in the present variable
boolean FLAG_inner = false;
boolean FLAG_outer = false;
boolean present = true;
boolean SENSOR_ON  = true; // used to determine whether the sensors should receive readings
uint8_t distance_inner = -1;
uint8_t distance_outer = -1;
int prev_time = 0;
int curr_time = 0;
int last_change = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  curr_time = millis();
  if(curr_time - prev_time >= INTERVAL && SENSOR_ON){
    prev_time = curr_time;
    FLAG_inner = false;
    FLAG_outer = false;
    
    // check distance
    distance_inner = sensor_inner.ping_cm();
    distance_outer = sensor_outer.ping_cm();

    Serial.print(distance_inner);
    Serial.print("\t");
    Serial.print(distance_outer);

    if(distance_inner - 38 < THRESHOLD){
      FLAG_inner = true;
    }
    if(distance_outer - 38 < THRESHOLD){
      FLAG_outer = true;
    }
    Serial.print("\t");
    Serial.print(FLAG_inner);
    Serial.print(", ");
    Serial.print(FLAG_outer);
    if(FLAG_inner && FLAG_outer){
      Serial.println("\tTRIGGERED");
    }
    else{
      Serial.println();
    }
    
  }
}
