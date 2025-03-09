from pose_tools import PoseTracker, PoseVisualizer
import cv2

if __name__ == "__main__":
  SCREEN_DIMS = (800, 800)

  capture = cv2.VideoCapture(0)

  # Make sure that the capture didn't fail to open
  if not capture.isOpened():
    print("Failed to open camera feed. Exiting the program.")
    exit()

  # Main program loop
  while True:
    ret, frame = capture.read()

    # Make sure that the frame data didn't fail to be read
    if not ret:
      print("Failed to receive data from camera feed. Exiting the program.")
      break

    # Resize the image
    frame = cv2.resize(frame, SCREEN_DIMS)

    # Extract pose data from the current frame
    image_landmarks, world_landmarks = PoseTracker.get_pose_from_image(frame)

    processed_frame = PoseVisualizer.show_pose(frame, image_landmarks, world_landmarks, SCREEN_DIMS)

    # Printing some messages on the screen for logging purposes
    if world_landmarks:
      # A box so that we can see the text
      processed_frame = cv2.rectangle(processed_frame, (0, 0), (SCREEN_DIMS[0], 100), (255, 255, 255), -1)

      # Checking if hands are closed or open
      # This may seem weird (LEFT is mapped to Right, while RIGHT is mapped to Left) but they are inverted (for some reason)
      left_hand = "closed" if PoseTracker.is_hand_grabbing(frame, 'Right') else "open"
      right_hand = "closed" if PoseTracker.is_hand_grabbing(frame, 'Left') else "open"
      text = f"LEFT HAND: {left_hand}, RIGHT HAND: {right_hand}"
      processed_frame = cv2.putText(processed_frame, text, (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

      # Finding the torso rotation
      text = f"TORSO: {PoseTracker.get_torso_rotation(world_landmarks=world_landmarks)}"
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
