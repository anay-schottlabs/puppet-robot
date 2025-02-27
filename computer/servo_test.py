import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Handle if the broker fails to connect
try:
  client.connect("localhost", 1883, 60)
except:
  print("Failed to connect to the MQTT broker. Exiting the program.")
  exit()

client.publish("robot/servos", "This is a test message from the computer")

client.disconnect()
