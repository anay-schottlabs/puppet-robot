from PCA9685 import PCA9685

# Needed for conversion from servo degrees to pulse (all of the values are in microseconds)
MIN_PULSE = 500
MAX_PULSE = 2500
BUFFER_PULSE = 50

# Values for controlling the claw at the end of each arm
CLAW_OPEN_PULSE = 2500 - BUFFER_PULSE
CLAW_CLOSE_PULSE = 500 + BUFFER_PULSE

class Servo:
  def __init__(self, max_degrees: int, channel: int):
    self.max_degrees = max_degrees
    self.channel = channel

# Servo channels for right arm
RIGHT_SHOULDER_FWD = Servo(max_degrees=180, channel=0)
RIGHT_SHOULDER_LAT = Servo(max_degrees=180, channel=1)
RIGHT_ELBOW_FWD = Servo(max_degrees=180, channel=2)
RIGHT_SHOULDER_LAT = Servo(max_degrees=180, channel=3)
RIGHT_CLAW = Servo(max_degrees=180, channel=4)

# Servo channels for left arm
LEFT_SHOULDER_FWD = Servo(max_degrees=180, channel=5)
LEFT_SHOULDER_LAT = Servo(max_degrees=180, channel=6)
LEFT_ELBOW_FWD = Servo(max_degrees=180, channel=7)
LEFT_ELBOW_LAT = Servo(max_degrees=180, channel=8)
LEFT_CLAW = Servo(max_degrees=180, channel=9)

# Servo channels for torso and head
HEAD_FWD = Servo(max_degrees=180, channel=10)
HEAD_LAT = Servo(max_degrees=180, channel=11)
TORSO = Servo(max_degrees=180, channel=12)

# The input from the pose tracking is in the form of angles in degrees
# We have to map these angles rotations of the servo, which are measured by their pulse width (in microseconds)
def servo_degrees_to_pulse(servo: Servo, degrees: int) -> int:
  # Calculate the factor
  factor = degrees / servo.max_degrees
  pulse_range = MAX_PULSE - MIN_PULSE
  pulse = factor * pulse_range + MIN_PULSE
  # Clamp the pulse between the min and max values
  if pulse < MIN_PULSE + BUFFER_PULSE:
    return MIN_PULSE + BUFFER_PULSE
  elif pulse > MAX_PULSE - BUFFER_PULSE:
    return MAX_PULSE - BUFFER_PULSE
  # The pulse was within the valid range so return it
  return pulse

if __name__ == "__main__":
  # pwm = PCA9685(0x40, debug=False)
  # pwm.setPWMFreq(50)
  # pwm.setServoPulse(channel=0, pulse=servo_degrees_to_pulse(180))

  # Take in data
  # Decode it into a readable format
  # Assign all of the servos to positions governed by the decoded values (converted from degrees into pulse)
  pass
