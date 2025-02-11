from pose import Point, Limb, Hand, Pose
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

class PoseTracker:
  @staticmethod
  def get_pose_from_image(image):
    # process pose, if none is detected end the method and return blank data (also include blank hand data)
    # if the pose exists in the image, extract hands and make up for hidden hands with blank data
    # extract the hand positions as a pose object

    # Convert the image to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create the necessary objects needed for pose detection
    base_options = python.BaseOptions(model_asset_path="pose_landmarker.task")
    options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
    detector = vision.PoseLandmarker.create_from_options(options)

    # Extract pose data from the processed image
    detection_result = detector.detect(image)
    pose_landmarks = detection_result.pose_landmarks

    # Convert the pose to a different format that only contains the necessary landmarks
    # Left arm
    left_shoulder = Point()
    left_elbow = Point()
    left_wrist = Point()

    # Left hand
    left_index_finger = Point()
    left_middle_finger = Point()
    left_ring_finger = Point()
    left_pinky_finger = Point()

    # Right arm
    right_shoulder = Point()
    right_elbow = Point()
    right_wrist = Point()

    # Right hand
    right_index_finger = Point()
    right_middle_finger = Point()
    right_ring_finger = Point()
    right_pinky_finger = Point()

    # Left leg
    left_hip = Point()
    left_knee = Point()
    left_foot = Point()

    # Right leg
    right_hip = Point()
    right_knee = Point()
    right_foot = Point()

    # Head
    head = Point()

    # Putting all of the points together
    left_arm = Limb()
    right_arm = Limb()
    left_leg = Limb()
    right_leg = Limb()

    left_hand = Hand()
    right_hand = Hand()

    # The entire pose represented as one object
    pose = Pose()

    return pose
