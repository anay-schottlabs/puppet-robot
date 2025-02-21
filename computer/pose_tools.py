import mediapipe as mp
import cv2
import math

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

class PoseVisualizer:
  @staticmethod
  def show_pose(image, image_landmarks, world_landmarks, screen_dims):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Copy the image
    image_with_pose = image.copy()
    screen_width, screen_height = screen_dims

    # Only show the pose on the image if the person is in the frame
    if image_landmarks:
      # Draw the basic connections between landmarks
      mp_drawing.draw_landmarks(image_with_pose, image_landmarks, mp_pose.POSE_CONNECTIONS)
      
      # This loop goes over the joints of the landmarks of the shoulder and elbow for both arms
      for i in range(11, 15):
        # x and y position of the landmark
        x = round(image_landmarks.landmark[i].x * screen_width)
        y = round(image_landmarks.landmark[i].y * screen_height)

        # Draw a circle around the landmark as a visual indicator that this will be sent to the robot
        image_with_pose = cv2.circle(image_with_pose, (x, y), 10, (255, 0, 0), -1)
        # Draw a rectangle next to the landmark to serve as a text box
        image_with_pose = cv2.rectangle(image_with_pose, (x, y), (x + 80, y - 30), (255, 255, 255), -1)

        # calculate the two angles of rotation for the joint
        angleXY, angleZY = PoseMath.get_joint_angles(world_landmarks, i)
        # add text to the text box that displays the calculated angles
        image_with_pose = cv2.putText(image_with_pose, f"XY: {angleXY}", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
        image_with_pose = cv2.putText(image_with_pose, f"ZY: {angleZY}", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
    return image_with_pose

class PoseMath:
  @staticmethod
  def get_relative_pos(start_point, end_point):
    # Unpack the XYZ values from each of the points
    start_x, start_y, start_z = start_point
    end_x, end_y, end_z = end_point
    # Get the end point's position relative to the position of the start point
    x = end_x - start_x
    y = end_y - start_y
    z = end_z - start_z
    return -x, -y, -z

  @staticmethod
  def get_joint_angles(world_landmarks, landmark_index):
    # This method gets the angles that a joint is rotated at
    # There are two angles because the shoulder and elbow can rotate along two different axes

    # First break up the landmarks into XYZ coordinates
    joint_point = (
      world_landmarks.landmark[landmark_index].x,
      world_landmarks.landmark[landmark_index].y,
      world_landmarks.landmark[landmark_index].z
    )
    end_point = (
      world_landmarks.landmark[landmark_index + 2].x,
      world_landmarks.landmark[landmark_index + 2].y,
      world_landmarks.landmark[landmark_index + 2].z
    )

    x, y, z = PoseMath.get_relative_pos(joint_point, end_point)

    # Solve for the angle on the XY plane
    angleXY = round(math.degrees(math.atan2(y, x)))
    # Solve for the angle on the ZY plane
    angleZY = round(math.degrees(math.atan2(y, z)))

    return angleXY, angleZY
