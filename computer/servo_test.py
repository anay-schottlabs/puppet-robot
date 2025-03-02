from dotenv import load_dotenv
from mqtt_publisher import MQTTPublisher
import sys, os

# Since the servo_data_format program is in the directory above, we have to append its path
sys.path.append('../puppet-robot')
from servo_data_format import ServoPose, TOPIC

# Load the Raspberry Pi's IP address from the .env file
load_dotenv()
RASPBERRY_PI_IP_ADDRESS = os.getenv("RASPBERRY_PI_IP_ADDRESS")

# This is a list of the servo values (angles in degrees)
# They are all defaulted to zero at the start of the program
DEFAULT_SERVO_LIST = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
servo_list = DEFAULT_SERVO_LIST

publisher = MQTTPublisher()
publisher.connect(broker_ip=RASPBERRY_PI_IP_ADDRESS)

print("Your inputs will control the robot's right arm servos.\n")

# Each number represents an index in the list of servos
servos = {
  "RIGHT SHOULDER FORWARD": 0,
  "LEFT SHOULDER FORWARD": 6,
  "TORSO": 14
}

was_zeros_sent = False

while True:
  # Get the values for every servo that is being tested
  for servo in servos.keys():
    while True:
      angle = input(f"{servo} (degrees): ")

      # Exit the program if 'exit' is inputted
      if angle == "exit":
        publisher.disconnect()
        exit()
      
      # Reset the value of all of the servos if 'zeros' is inputted
      if angle == "zeros":
        was_zeros_sent = True
        break

      # Make sure that the inputted value is an integer
      try:
        servo_list[servos[servo]] = int(angle)
        break
      except:
        print("Value must be an integer.")
    
    if was_zeros_sent:
      servo_list = DEFAULT_SERVO_LIST
      was_zeros_sent = False
      break
  
  # Convert the list of servos into a pose object and send it
  servo_pose = ServoPose(*servo_list)
  publisher.publish_message(topic=TOPIC, message=servo_pose.to_sendable())
  print("\n")
