from pose_tools import PoseTracker, PoseVisualizer
import cv2
from threading import Thread, Lock
from time import sleep
from mqtt_publisher import MQTTPublisher
from dotenv import load_dotenv
import sys, os

# Since the servo_data_format program is in the directory above, we have to append its path
sys.path.append('../puppet-robot')
from servo_data_format import ServoPose, TOPIC

# Load the Raspberry Pi's IP address from the .env file
load_dotenv()
RASPBERRY_PI_IP_ADDRESS = os.getenv("RASPBERRY_PI_IP_ADDRESS")

# This is a list of the servo values (angles in degrees)
# They are all defaulted to zero at the start of the program
servo_pose = ServoPose(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

kill_next_cycle = False
CYCLE_DELAY_SECONDS = 5
lock = Lock()

def publish_messages():
  publisher = MQTTPublisher()
  publisher.connect(broker_ip=RASPBERRY_PI_IP_ADDRESS)

  while not kill_next_cycle:
    # Have some delay so that we don't have an uncontrolled amount of messages
    sleep(CYCLE_DELAY_SECONDS)
    with lock:
      # Send the servo pose over to the Raspberry Pi
      publisher.publish_message(topic=TOPIC, message=servo_pose.to_sendable())
  
  publisher.disconnect()
  print("Closing message publishing thread. The program will now exit.")

if __name__ == "__main__":
  SCREEN_DIMS = (800, 800)

  capture = cv2.VideoCapture(0)
  
  publish_thread = Thread(target=publish_messages)
  publish_thread.start()

  # Main program loop
  while True:
    # Make sure that the capture didn't fail to open
    if not capture.isOpened():
      print("Failed to open camera feed. Exiting the program.")
      break

    ret, frame = capture.read()

    # Make sure that the frame data didn't fail to be read
    if not ret:
      print("Failed to receive data from camera feed. Exiting the program.")
      break

    # Resize the image
    frame = cv2.resize(frame, SCREEN_DIMS)

    # Extract pose data from the current frame
    image_landmarks, world_landmarks = PoseTracker.get_pose_from_image(frame)

    processed_frame = PoseVisualizer.show_pose(frame, image_landmarks)

    if world_landmarks:
      # Have to make sure that the lock is not acquired
      # This is needed to ensure that there is no conflict between the main thread writing to the servo pose while the publish thread is reading from it
      if not lock.locked():
        # MAIN CALCULATIONS

        # Torso
        servo_pose.torso = PoseTracker.get_torso_rotation(world_landmarks=world_landmarks)

        # Head
        servo_pose.head_fwd, servo_pose.head_lat = PoseTracker.get_head_rotation(
          world_landmarks=world_landmarks,
          torso_rotation=servo_pose.torso
        )

        # Arm rotations
        servo_pose.right_shoulder_fwd, servo_pose.right_shoulder_lat, servo_pose.right_elbow_fwd = PoseTracker.get_arm_rotations(
          world_landmarks=world_landmarks,
          is_left_arm=False,
          torso_rotation=servo_pose.torso
        )

        servo_pose.left_shoulder_fwd, servo_pose.left_shoulder_lat, servo_pose.left_elbow_fwd = PoseTracker.get_arm_rotations(
          world_landmarks=world_landmarks,
          is_left_arm=True,
          torso_rotation=servo_pose.torso
        )
        
        # Hands
        # This may seem weird (left is mapped to right, while right is mapped to left), but the handedness values seem to be inverted as of my testing
        is_left_hand_closed = PoseTracker.is_hand_grabbing(frame, "Right")
        servo_pose.left_claw = ServoPose.CLAW_CLOSE_DEGREES if is_left_hand_closed else ServoPose.CLAW_OPEN_DEGREES
        is_right_hand_closed = PoseTracker.is_hand_grabbing(frame, "Left")
        servo_pose.right_claw = ServoPose.CLAW_CLOSE_DEGREES if is_right_hand_closed else ServoPose.CLAW_OPEN_DEGREES

        # LOGGING
        # A box so that we can see the text
        processed_frame = cv2.rectangle(processed_frame, (0, 0), (SCREEN_DIMS[0], 100), (255, 255, 255), -1)

        # Checking if hands are closed or open
        # This may seem weird (LEFT is mapped to Right, while RIGHT is mapped to Left) but they are inverted (for some reason)
        left_hand = "closed" if is_left_hand_closed else "open"
        right_hand = "closed" if is_right_hand_closed else "open"
        text = f"LEFT HAND: {left_hand}, RIGHT HAND: {right_hand}"
        processed_frame = cv2.putText(processed_frame, text, (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        # Finding the torso rotation
        text = f"TORSO: {servo_pose.torso}"
        processed_frame = cv2.putText(processed_frame, text, (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # Display the current frame image after it has been processed
    cv2.imshow("Pose Tracking", processed_frame)

    # Exit the program if the Q key is pressed
    if cv2.waitKey(1) == ord("q"):
      print("Q key was pressed, exiting the program.")
      break

  # Release the capture and close the window once the program is finished
  capture.release()
  cv2.destroyAllWindows()
  kill_next_cycle = True
