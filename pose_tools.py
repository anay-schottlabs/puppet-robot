import mediapipe as mp
import cv2
import math
import json

# Load default pose data
with open("default_world_landmarks.json", "r") as file:
  DEFAULT_WORLD_LANDMARKS = json.load(file)

class PoseTracker:
  @staticmethod
  def get_pose_from_image(image):
    # Convert the image to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Extract pose data from the processed image
    mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5)
    pose_detection_result = mp_pose.process(image_rgb)
    image_landmarks = pose_detection_result.pose_landmarks
    world_landmarks = pose_detection_result.pose_world_landmarks
    
    # If no one is in the frame, use the default world landmarks
    if world_landmarks:
      world_landmarks = world_landmarks.landmark
    else:
      world_landmarks = DEFAULT_WORLD_LANDMARKS

    return image_landmarks, world_landmarks

class PoseVisualizer:
  @staticmethod
  def show_pose(image, pose_landmarks, screen_dims):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Copy the image
    image_with_pose = image.copy()
    screen_width, screen_height = screen_dims

    # show pose on the image
    for i in range(11, 17):
      # Only show the pose on the image if the person is in the frame
      if pose_landmarks:
        mp_drawing.draw_landmarks(image_with_pose, pose_landmarks, mp_pose.POSE_CONNECTIONS)
        x = round(pose_landmarks.landmark[i].x * screen_width)
        y = round(pose_landmarks.landmark[i].y * screen_height)
        image_with_pose = cv2.circle(image_with_pose, (x, y), 10, (255, 0, 0), -1)

    return image_with_pose

class PoseMath:
  @staticmethod
  def get_relative_pos(start_point, end_point):
    # Have to access the values differently depending on if the default pose values are being used or not
    if isinstance(start_point, dict):
      start_x = start_point["x"]
      start_y = start_point["y"]
      end_x = end_point["x"]
      end_y = end_point["y"]
    else:
      start_x = start_point.x
      start_y = start_point.y
      end_x = end_point.x
      end_y = end_point.y
    # Get the end point's position relative to the position of the start point
    x = end_x - start_x
    y = end_y - start_y
    return -x, -y
  
  @staticmethod
  def get_joint_angle(joint_point, end_point):
    # Get the angle that the joint is rotated at
    # This will be useful for figuring out the rotations that the servos will be mapped to
    x, y = PoseMath.get_relative_pos(joint_point, end_point)
    return math.degrees(math.atan2(y, x))
