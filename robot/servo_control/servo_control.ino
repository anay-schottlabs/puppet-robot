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

const Servo RIGHT_SHOULDER_FWD = Servo(0, 360);
const Servo RIGHT_SHOULDER_LAT = Servo(1, 360);
const Servo RIGHT_ELBOW_FWD = Servo(2, 180);
const Servo RIGHT_ELBOW_LAT = Servo(3, 180);
const Servo RIGHT_WRIST = Servo(4, 180);
const Servo RIGHT_CLAW = Servo(5, 180);
const Servo LEFT_SHOULDER_FWD = Servo(6, 360);
const Servo LEFT_SHOULDER_LAT = Servo(7, 360);
const Servo LEFT_ELBOW_FWD = Servo(8, 180);
const Servo LEFT_ELBOW_LAT = Servo(9, 180);
const Servo LEFT_WRIST = Servo(10, 180);
const Servo LEFT_CLAW = Servo(11, 180);
const Servo HEAD_FWD = Servo(12, 180);
const Servo HEAD_LAT = Servo(13, 180);
const Servo TORSO = Servo(14, 360);

void setup() {
  Serial.begin(115200);
  // pwm.begin();
  // pwm.setOscillatorFrequency(27000000);
  // pwm.setPWMFreq(Servo::SERVO_FREQ);

  delay(10);

  // servo1.setServoDegrees(0);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop() {
  while (!Serial.available());

  int jointAngles[15] = {};

  String message = Serial.readString();
  int lastDelimIndex = 0;

  for (int i = 0; i < 15; i++) {
    if (i != 14) {
      int substringEnd = message.indexOf(" ", lastDelimIndex + 1);
      jointAngles[i] = message.substring(lastDelimIndex, substringEnd).toInt();
      lastDelimIndex = substringEnd;
    }
    else jointAngles[i] = message.substring(lastDelimIndex).toInt();
  }

  if (jointAngles[RIGHT_SHOULDER_FWD] == 180) {
    digitalWrite(13, HIGH);
  }
  else if (jointAngles[RIGHT_SHOULDER_FWD] == 0) {
    digitalWrite(13, LOW);
  }
}
