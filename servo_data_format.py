from typing import Self

# This class serves as an outline for transmitting servo data between the computer and the Raspberry Pi
class ServoPose:
  CLAW_OPEN_DEGREES = 180
  CLAW_CLOSE_DEGREES = 0

  def __init__(
      self,
      right_shoulder_fwd: int,
      right_shoulder_lat: int,
      right_elbow_fwd: int,
      right_elbow_lat: int,
      right_wrist: int,
      right_claw: int,
      left_shoulder_fwd: int,
      left_shoulder_lat: int,
      left_elbow_fwd: int,
      left_elbow_lat: int,
      left_wrist: int,
      left_claw: int,
      head_fwd: int,
      head_lat: int,
      torso: int
  ):
    self.right_shoulder_fwd = right_shoulder_fwd
    self.right_shoulder_lat = right_shoulder_lat
    self.right_elbow_fwd = right_elbow_fwd
    self.right_elbow_lat = right_elbow_lat
    self.right_wrist = right_wrist
    self.right_claw = right_claw
    self.left_shoulder_fwd = left_shoulder_fwd
    self.left_shoulder_lat = left_shoulder_lat
    self.left_elbow_fwd = left_elbow_fwd
    self.left_elbow_lat = left_elbow_lat
    self.left_wrist = left_wrist
    self.left_claw = left_claw
    self.head_fwd = head_fwd
    self.head_lat = head_lat
    self.torso = torso
  
  # This converts the data into a string so that it can be sent
  def to_sendable(self) -> str:
    servos = vars(self)
    return " ".join([str(servo[1]) for servo in servos.items()])
  
  # This converts the stringified data into a ServoPose object so that it can be read from
  @staticmethod
  def from_sendable(sendable: str) -> Self:
    data = [ int(angle) for angle in sendable.split(" ") ]
    return ServoPose(*data)

TOPIC = "robot/servos"
