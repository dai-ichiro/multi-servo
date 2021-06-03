#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN 165 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 455 // this is the 'maximum' pulse length count (out of 4096)

#define servo_count 4

Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);

void setup() {
  Serial.begin(9600);
  pwm1.begin();
  pwm1.setPWMFreq(50);

  servo_write(0, 90);
  servo_write(1, 90);
  servo_write(2, 90);
  servo_write(3, 90);
}

void loop() {
  if(Serial.available()> (2*servo_count - 1)){
    int serial_no;
    int servo_1_now;
    int servo_2_now;
    int servo_3_now;
    int servo_4_now;

    for(int i=0; i<servo_count; i++){
      serial_no = Serial.read();
      if(serial_no > 200){
        if(serial_no == 201){
          servo_1_now = Serial.read();
        }
        if(serial_no == 202){
          servo_2_now = Serial.read();
        }
        if(serial_no == 203){
          servo_3_now = Serial.read();
        }
        if(serial_no == 204){
          servo_4_now = Serial.read();
        }
      }
    }
    servo_write(0, servo_1_now);
    servo_write(1, servo_2_now);
    servo_write(2, servo_3_now);
    servo_write(3, servo_4_now);
    delay(40);
    Serial.write(255);
  }
}

void servo_write(int ch, int ang){
  ang = map(ang, 0, 180, SERVOMIN, SERVOMAX);
  pwm1.setPWM(ch, 0, ang);
}
