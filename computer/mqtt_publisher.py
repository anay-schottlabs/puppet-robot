import paho.mqtt.client as mqtt

class MQTTPublisher:
  def __init__(self) -> None:
    self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
  
  def connect(self, broker_ip: str) -> None:
    try:
      self.client.connect(broker_ip, 1883, 60)
    except:
      raise ConnectionError("Failed to connect to the broker.")
  
  def disconnect(self):
    self.client.disconnect()
  
  def publish_message(self, topic: str, message: str):
    self.client.publish(topic, message)
