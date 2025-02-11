class Point:
  def __init__(self, worldX, worldY, worldZ, imgX, imgY):
    self. worldX = worldX
    self.worldY = worldY
    self.worldZ = worldZ
    self.imgX = imgX
    self.imgY = imgY

class Limb:
  def __init__(self, base_joint, mid_joint, end_point):
    self.base_joint = base_joint
    self.mid_joint = mid_joint
    self.end_point = end_point
  
  def get_base_joint_angle(self):
    # write code here
    pass

  def get_mid_joint_angle(self):
    # write code here (use the end point to calculate the angle)
    pass

class Hand:
  def __init__(self, index_finger, middle_finger, ring_finger, pinky_finger):
    self.index_finger = index_finger
    self.middle_finger = middle_finger
    self.ring_finger = ring_finger
    self.pinky_finger = pinky_finger

  def is_grabbing(self):
    # write code here
    pass

class Pose:
  def __init__(self, left_arm, right_arm, left_hand, right_hand, left_leg, right_leg, head):
    self.left_arm = left_arm
    self.right_arm = right_arm
    self.left_hand = left_hand
    self.right_hand = right_hand
    self.left_leg = left_leg
    self.right_leg = right_leg
    self.head = head
