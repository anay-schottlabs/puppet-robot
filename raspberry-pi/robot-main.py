from PCA9685 import PCA9685

# Important constants for servo control
MAX_SERVO_DEGREES = 180
MIN_PULSE_MICROSECONDS = 500
MAX_PULSE_MICROSECONDS = 2500

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
