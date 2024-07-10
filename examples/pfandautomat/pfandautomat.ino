
#include "Grove_I2C_Motor_Driver.h"

#define I2C_ADDRESS 0x0f

#include <FastLED.h>

#define NUM_LEDS 5

#define DATA_PIN 6

CRGB leds[NUM_LEDS];

const int buttonStartPin = 2;
const int inputCodeValidPin = 3;

void setup() {
  delay(1000);
  Serial.begin(115200);
  delay(1000);
  Serial.println("Pfandautomat");

  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);

  pinMode(buttonStartPin, INPUT_PULLUP);
  pinMode(inputCodeValidPin, INPUT);


  Motor.begin(I2C_ADDRESS);

  //move_bottle_in();
  set_leds_off();

  Serial.println("go..");
}

void loop() {
  // set_leds_white();
  // delay(1000);
  // set_leds_green();
  // delay(1000);
  // set_leds_red();
  // delay(1000);

  if (digitalRead(buttonStartPin) == LOW) {
    Serial.println("move in..");
    set_leds_white();
    move_bottle_in();
    bottle_scan();
  }
}



void set_leds_white() {
  fill_solid(leds, NUM_LEDS, CRGB(255, 255, 255));
  FastLED.show();
}

void set_leds_green() {
  fill_solid(leds, NUM_LEDS, CRGB(0, 255, 0));
  FastLED.show();
}

void set_leds_red() {
  fill_solid(leds, NUM_LEDS, CRGB(255, 0, 0));
  FastLED.show();
}

void set_leds_off() {
  fill_solid(leds, NUM_LEDS, CRGB(0, 0, 0));
  FastLED.show();
}



void move_bottle_in() {
  Motor.speed(MOTOR1, 255);
  delay(2000);
  Motor.stop(MOTOR1);
}

void move_bottle_out() {
  Motor.speed(MOTOR1, 255);
  delay(2000);
  Motor.stop(MOTOR1);
}

void move_bottle_container() {
  Motor.speed(MOTOR1, 255);
  delay(2000);
  Motor.stop(MOTOR1);
}


void bottle_scan() {
  Serial.println("bottle_scan");
  Motor.speed(MOTOR2, 255);

  bool waiting = true;
  uint32_t start_time = millis();
  while (waiting) {
    if (digitalRead(inputCodeValidPin) == HIGH) {
      waiting = false;
      Motor.stop(MOTOR2);
      Serial.println("bottle valid");
      move_bottle_container();
    } else {
      uint32_t duration = millis() - start_time;
      if (duration > 3000) {
        Serial.println("timeout");
        Motor.stop(MOTOR2);
        move_bottle_out();
        waiting = false;
      }
    }
  }
}
