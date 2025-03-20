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
    return result + 360 if result < 0 else result
  
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
  def get_shoulder_rotations(world_landmarks, landmark_index, forward_signs, lateral_signs, fwd_y_first, lat_y_first, torso_rotation):
    # This method gets the angles that a joint is rotated at
    # There are two angles because the shoulder can rotate along two different axes

    multiplier = 100

    # First break up the landmarks into XYZ coordinates, and make sure that they are not affected by the rotation of the torso
    joint_point = PoseMath.cancel_torso_rotation([
      world_landmarks.landmark[landmark_index].x,
      world_landmarks.landmark[landmark_index].y,
      world_landmarks.landmark[landmark_index].z
    ], torso_rotation)

    end_point = PoseMath.cancel_torso_rotation([
      world_landmarks.landmark[landmark_index + 2].x,
      world_landmarks.landmark[landmark_index + 2].y,
      world_landmarks.landmark[landmark_index + 2].z
    ], torso_rotation)

    # Then get the relative position
    x, y, z = PoseMath.get_relative_pos_3d(joint_point, end_point)

    # Change the values based on the provided signs
    x = x * math.copysign(1, forward_signs[0])
    y = y * math.copysign(1, forward_signs[1])
    z = z * math.copysign(1, forward_signs[2])

    # Calculations for the forward angle
    if fwd_y_first:
      forward = round(math.degrees(math.atan2(y, x)))
    else:
      forward = round(math.degrees(math.atan2(x, y)))
    forward += 360 if forward < 0 else 0

    # Change the values based on the provided signs
    x = x * math.copysign(1, lateral_signs[0])
    y = y * math.copysign(1, lateral_signs[1])
    z = z * math.copysign(1, lateral_signs[2])

    # Calculations for the lateral angle
    if lat_y_first:
      lateral = round(math.degrees(math.atan2(y, z)))
    else:
      lateral = round(math.degrees(math.atan2(z, y)))
    lateral += 360 if lateral < 0 else 0

    return forward, lateral

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
