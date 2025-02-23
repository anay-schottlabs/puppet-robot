from PCA9685 import PCA9685

# Needed for conversion from servo degrees to pulse
MAX_SERVO_DEGREES = 180
MIN_PULSE_MICROSECONDS = 500
MAX_PULSE_MICROSECONDS = 2500

# Values for controlling the claw at the end of each arm
CLAW_OPEN_PULSE = 2500
CLAW_CLOSE_PULSE = 500

# Servo channels for right arm
RIGHT_SHOULDER_FWD = 0
RIGHT_SHOULDER_LAT = 1
RIGHT_ELBOW_FWD = 2
RIGHT_SHOULDER_LAT = 3
RIGHT_CLAW = 4

# Servo channels for left arm
LEFT_SHOULDER_FWD = 5
LEFT_SHOULDER_LAT = 6
LEFT_ELBOW_FWD = 7
LEFT_ELBOW_LAT = 8
LEFT_CLAW = 9

# The input from the pose tracking is in the form of angles in degrees
# We have to map these angles rotations of the servo, which are measured by their pulse width (in microseconds)
def servo_degrees_to_pulse(degrees):
  # Calculate the factor
  factor = degrees / MAX_SERVO_DEGREES
  pulse_range = MAX_PULSE_MICROSECONDS - MIN_PULSE_MICROSECONDS
  pulse = factor * pulse_range + MIN_PULSE_MICROSECONDS
  # Clamp the pulse between the min and max values
  if pulse < MIN_PULSE_MICROSECONDS:
    return MIN_PULSE_MICROSECONDS
  elif pulse > MAX_PULSE_MICROSECONDS:
    return MAX_PULSE_MICROSECONDS
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
