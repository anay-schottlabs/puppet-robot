from PCA9685 import PCA9685
import sys

# Since the servo_data_format program is in the directory above, we have to append its path
sys.path.append('../puppet-robot')
from servo_data_format import ServoPose

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
RIGHT_SHOULDER_FWD = Servo(max_degrees=360, channel=0)
RIGHT_SHOULDER_LAT = Servo(max_degrees=360, channel=1)
RIGHT_ELBOW_FWD = Servo(max_degrees=180, channel=2)
RIGHT_ELBOW_LAT = Servo(max_degrees=180, channel=3)
RIGHT_WRIST = Servo(max_degrees=180, channel=4)
RIGHT_CLAW = Servo(max_degrees=180, channel=5)

# Servo channels for left arm
LEFT_SHOULDER_FWD = Servo(max_degrees=360, channel=6)
LEFT_SHOULDER_LAT = Servo(max_degrees=360, channel=7)
LEFT_ELBOW_FWD = Servo(max_degrees=180, channel=8)
LEFT_ELBOW_LAT = Servo(max_degrees=180, channel=9)
LEFT_WRIST = Servo(max_degrees=180, channel=10)
LEFT_CLAW = Servo(max_degrees=180, channel=11)

# Servo channels for torso and head
HEAD_FWD = Servo(max_degrees=180, channel=12)
HEAD_LAT = Servo(max_degrees=180, channel=13)
TORSO = Servo(max_degrees=360, channel=14)

# Set up the PWM controller
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

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

# A method to set the pulse of a servo
def set_servo_angle(servo: Servo, degrees: int) -> None:
  pulse = servo_degrees_to_pulse(servo=servo, degrees=degrees)
  pwm.setServoPulse(servo.channel, pulse)

# This method will be used as a callback for the data_receiver program
def set_servos(servo_pose: ServoPose):
  set_servo_angle(RIGHT_SHOULDER_FWD, servo_pose.right_shoulder_fwd)
  set_servo_angle(RIGHT_SHOULDER_LAT, servo_pose.right_shoulder_lat)
  set_servo_angle(RIGHT_ELBOW_FWD, servo_pose.right_elbow_fwd)
  set_servo_angle(RIGHT_ELBOW_LAT, servo_pose.right_elbow_lat)
  set_servo_angle(RIGHT_WRIST, servo_pose.right_wrist)
  set_servo_angle(RIGHT_CLAW, servo_pose.right_claw)
  set_servo_angle(LEFT_SHOULDER_FWD, servo_pose.left_shoulder_fwd)
  set_servo_angle(LEFT_SHOULDER_LAT, servo_pose.left_shoulder_lat)
  set_servo_angle(LEFT_ELBOW_FWD, servo_pose.left_elbow_fwd)
  set_servo_angle(LEFT_ELBOW_LAT, servo_pose.left_elbow_lat)
  set_servo_angle(LEFT_WRIST, servo_pose.left_wrist)
  set_servo_angle(LEFT_CLAW, servo_pose.left_claw)
