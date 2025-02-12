import mediapipe as mp
import cv2

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
