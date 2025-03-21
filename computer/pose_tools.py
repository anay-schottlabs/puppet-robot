import mediapipe as mp
import cv2
import math
import numpy as np
from scipy.spatial.transform import Rotation as R

class PoseTracker:
  @staticmethod
  def get_pose_from_image(image):
    # Convert the image to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Extract pose data from the processed image
    mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.75)
    pose_detection_result = mp_pose.process(image_rgb)
    image_landmarks = pose_detection_result.pose_landmarks
    world_landmarks = pose_detection_result.pose_world_landmarks

    return image_landmarks, world_landmarks
  
  @staticmethod
  def is_hand_grabbing(image, hand_label):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.75, max_num_hands=2)
    result = mp_hands.process(image_rgb)

    if result.multi_hand_landmarks:
      for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
        handedness = result.multi_handedness[i]
        label = handedness.classification[0].label
        if label == hand_label:
          wrist = [
            hand_landmarks.landmark[0].x,
            hand_landmarks.landmark[0].y
          ]
          reference = [
            hand_landmarks.landmark[10].x,
            hand_landmarks.landmark[10].y
          ]
          finger = [
            hand_landmarks.landmark[12].x,
            hand_landmarks.landmark[12].y
          ]
          reference_dist = math.dist(finger, reference)
          wrist_dist = math.dist(finger, wrist)
          if (wrist_dist < reference_dist):
            return True
          return False
    return True
  
  @staticmethod
  def get_torso_rotation(world_landmarks):
    # Here, Z is forward to backward, Y is up to down, and X is left to right
    # We're looking at this from a top-down perspective, so the Z value will replace the Y value
    left_hip = [
      world_landmarks.landmark[23].x,
      world_landmarks.landmark[23].z
    ]
    right_hip = [
      world_landmarks.landmark[24].x,
      world_landmarks.landmark[24].z
    ]
    x, y = PoseMath.get_relative_pos_2d(right_hip, left_hip)
    # This calculates the actual angle, with 0 degrees representing the person facing right
    result = round(math.degrees(math.atan2(y, x)))
    return round((result + 360 if result < 0 else result) / 2)
  
  @staticmethod
  def get_head_rotation(world_landmarks, torso_rotation):
    mouth = [
      world_landmarks.landmark[10].z,
      world_landmarks.landmark[10].y,
    ]
    eyebrow = [
      world_landmarks.landmark[4].z,
      world_landmarks.landmark[4].y,
    ]
    forward_x, forward_y = PoseMath.get_relative_pos_2d(mouth, eyebrow)
    forward = round(math.degrees(math.atan2(-forward_y, forward_x)) + 160)

    left_ear = PoseMath.cancel_torso_rotation([
      world_landmarks.landmark[7].x,
      world_landmarks.landmark[7].z,
      0
    ], torso_rotation)
    right_ear = PoseMath.cancel_torso_rotation([
      world_landmarks.landmark[8].x,
      world_landmarks.landmark[8].z,
      0
    ], torso_rotation)
    lateral_x, lateral_y = PoseMath.get_relative_pos_2d(right_ear[0::2], left_ear[0::2])
    lateral = round(math.degrees(math.atan2(lateral_y, lateral_x)))
    lateral = round((lateral + 360 if lateral < 0 else lateral) / 2)
    return forward, lateral * 2
  
  @staticmethod
  def get_arm_rotations(world_landmarks, is_left_arm, torso_rotation):
    # This method computes inverse kinematics for the entire arm
    # There are two angles because the shoulder can rotate along two different axes

    # Determine what the landmark index of the wrist is based on if we are processing the left or right arm
    if is_left_arm:
      wrist_index = 15
    else:
      wrist_index = 16

    # Find the end effector position and make sure it's not affected by the torso rotation
    wrist = PoseMath.cancel_torso_rotation([
      world_landmarks.landmark[wrist_index].x,
      world_landmarks.landmark[wrist_index].y,
      world_landmarks.landmark[wrist_index].z
    ], torso_rotation)

    # Find the end effector position and make sure it's not affected by the torso rotation
    shoulder = PoseMath.cancel_torso_rotation([
      world_landmarks.landmark[wrist_index - 4].x,
      world_landmarks.landmark[wrist_index - 4].y,
      world_landmarks.landmark[wrist_index - 4].z
    ], torso_rotation)

    # Get the relative position of the wrist from the shoulder
    x, y, z = PoseMath.get_relative_pos_3d(shoulder, wrist)

    # The position is a vector, so we'll normalize it to make calculations simpler
    end_pos = np.array([x, y, z])
    norm = np.linalg.norm(end_pos)
    end_pos = end_pos / norm

    x, y, z = end_pos

    # Mirror the X coordinate for the left arm
    if is_left_arm:
      x = -x

    # Inverse kinematics calculations
    shoulder_lat = math.atan2(z, x) * (180 / math.pi)
    l = math.sqrt(x * x + z * z)
    h = math.sqrt(l * l + y * y)
    phi = math.atan(y / l) * (180 / math.pi)
    theta = math.acos((h / 2) / 0.5) * (180 / math.pi)

    # Account for completely vertical positions
    if l == 0:
      shoulder_fwd = 0
      elbow_fwd = 0
      shoulder_lat = phi
    else:
      shoulder_fwd = phi + theta
      elbow_fwd = phi - theta

    shoulder_lat = 90 - shoulder_lat

    # Adjust shoulder_fwd for 0 to 180 range
    if shoulder_fwd < 0:
      shoulder_fwd = 180 + shoulder_fwd

    # More value tuning to account for the zero position of the left arm
    if is_left_arm:
      shoulder_lat = 180 - shoulder_lat
      shoulder_fwd = -shoulder_fwd
      elbow_fwd = 90 - elbow_fwd

    return shoulder_fwd, shoulder_lat, min(elbow_fwd, 90) # Clamp elbow rotation to a max of 90 (due to physical robot limitations)

class PoseVisualizer:
  @staticmethod
  def show_pose(image, image_landmarks):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Copy the image
    image_with_pose = image.copy()

    # Only show the pose on the image if the person is in the frame
    if image_landmarks:
      # Draw the basic connections between landmarks
      mp_drawing.draw_landmarks(image_with_pose, image_landmarks, mp_pose.POSE_CONNECTIONS)
    return image_with_pose

class PoseMath:
  @staticmethod
  def get_relative_pos_3d(start_point, end_point):
    # Unpack the XYZ values from each of the points
    start_x, start_y, start_z = start_point
    end_x, end_y, end_z = end_point
    # Get the end point's position relative to the position of the start point
    x = end_x - start_x
    y = end_y - start_y
    z = end_z - start_z
    return -x, -y, -z
  
  @staticmethod
  def get_relative_pos_2d(start_point, end_point):
    # Unpack the XY values from each of the points
    start_x, start_y = start_point
    end_x, end_y = end_point
    # Get the end point's position relative to the position of the start point
    x = end_x - start_x
    y = end_y - start_y
    return -x, -y
  
  @staticmethod
  def cancel_torso_rotation(point, torso_rotation):
    multiplier = 100
    rotation = R.from_euler("y", torso_rotation / 2, degrees=True)
    point_np = np.array(point) * multiplier
    return np.round(rotation.apply(point_np))
