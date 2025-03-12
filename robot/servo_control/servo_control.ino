#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

class Servo {
  public:
    int channel;
    int maxDegrees;
    const static int SERVO_FREQ = 50;

    Servo(int channelParam, int maxDegreesParam) {
      channel = channelParam;
      maxDegrees = maxDegreesParam;
    }

    void setServoDegrees(int degrees) {
      int constrainedDegrees = constrain(degrees, 0, maxDegrees);
      int pulse = map(constrainedDegrees, 0, maxDegrees, Servo::PULSE_MIN, Servo::PULSE_MAX);
      pwm.writeMicroseconds(channel, pulse);
    }
  
  private:
    // These are measured in microseconds
    const static int PULSE_MIN = 600;
    const static int PULSE_MAX = 2400;
};

Servo servo1 = Servo(0, 180);

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(Servo::SERVO_FREQ);

  delay(10);
}

void loop() {
  servo1.setServoDegrees(0);
  delay(2000);
  servo1.setServoDegrees(90);
  delay(2000);
  servo1.setServoDegrees(180);
  delay(2000);
}
