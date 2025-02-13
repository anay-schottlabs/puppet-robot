import mediapipe as mp
import cv2
import math

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

    return image_landmarks, world_landmarks

class PoseVisualizer:
  @staticmethod
  def show_pose(image, pose_landmarks):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Draw the pose landmarks on the image
    image_with_pose = image.copy()
    mp_drawing.draw_landmarks(image_with_pose, pose_landmarks, mp_pose.POSE_CONNECTIONS)

    return image_with_pose

class PoseMath:
  @staticmethod
  def get_relative_pos(start_point, end_point):
    # Get the end point's position relative to the position of the start point
    x = end_point.x - start_point.x
    y = end_point.y - start_point.y
    return x, y
  
  @staticmethod
  def get_joint_angle(joint_point, end_point):
    # Get the angle that the joint is rotated at
    # This will be useful for figuring out the rotations that the servos will be mapped to
    x, y = PoseMath.get_relative_pos(joint_point, end_point)
    return math.degrees(math.atan2(y, x))
