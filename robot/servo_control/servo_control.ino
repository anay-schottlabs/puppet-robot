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

const Servo SERVOS[] = {
  Servo(0, 360), // RIGHT_SHOULDER_FWD
  Servo(1, 360), // RIGHT_SHOULDER_LAT
  Servo(2, 180), // RIGHT_ELBOW_FWD
  Servo(3, 180), // RIGHT_ELBOW_LAT
  Servo(4, 180), // RIGHT_WRIST
  Servo(5, 180), // RIGHT_CLAW
  Servo(6, 360), // LEFT_SHOULDER_FWD
  Servo(7, 360), // LEFT_SHOULDER_LAT
  Servo(8, 180), // LEFT_ELBOW_FWD
  Servo(9, 180), // LEFT_ELBOW_LAT
  Servo(10, 180), // LEFT_WRIST
  Servo(11, 180), // LEFT_CLAW
  Servo(12, 180), // HEAD_FWD
  Servo(13, 180), // HEAD_LAT
  Servo(14, 360) // TORSO
};

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(Servo::SERVO_FREQ);

  delay(10);

  pinMode(13, OUTPUT);
}

void loop() {
  // Turn the LED off if we don't have a signal, keep it on if we do
  while (!Serial.available()) {
    digitalWrite(13, LOW);
  }
  digitalWrite(13, HIGH);

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

  for (Servo servo : SERVOS) {
    servo.setServoDegrees(jointAngles[servo.channel]);
  }
}
