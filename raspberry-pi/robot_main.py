import paho.mqtt.client as mqtt
from servo_control import set_servos
import sys

# Since the servo_data_format program is in the directory above, we have to append its path
sys.path.append('../puppet-robot')
from servo_data_format import ServoPose, TOPIC

client = mqtt.Client()

def on_connect(client, userdata, flags, rc) -> None:
  # Handle broker connection failure
  if rc != 0:
    print("Failed to connect to the broker. Exiting the program.")
    exit()
  print("Connected to the broker.")
  client.subscribe(TOPIC)

# When the message is received, emulate the servo angles on the robot
def on_message(client, userdata, message) -> None:
  print(f"Received Message: {message.payload}")
  print("Emulating pose on robot...\n")
  set_servos(servo_pose=ServoPose.from_sendable(message.payload.decode("utf-8")))

def on_subscribe(client, userdata, mid, granted_qos) -> None:
  print(f"Subscribed to the topic '{TOPIC}'.")

# Define the callbacks for certain events
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Handle broker connection failure
try:
  client.connect("localhost", 1883, 63)
except:
  print("Failed to connect to the broker. Exiting the program.")
  exit()

client.loop_forever()
