from typing import Self

# This class serves as an outline for transmitting servo data between the computer and the Raspberry Pi
class ServoPose:
  def __init__(
      self,
      right_shoulder_fwd,
      right_shoulder_lat,
      right_elbow_fwd,
      right_elbow_lat,
      right_wrist,
      right_claw,
      left_shoulder_fwd,
      left_shoulder_lat,
      left_elbow_fwd,
      left_elbow_lat,
      left_wrist,
      left_claw,
      head_fwd,
      head_lat,
      torso
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
  def from_sendable(sendable) -> Self:
    data = sendable.split(" ")
    return ServoPose(*data)
