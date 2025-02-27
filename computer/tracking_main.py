from pose_tools import PoseTracker, PoseVisualizer, PoseMath
import cv2

if __name__ == "__main__":
  SCREEN_DIMS = (800, 800)

  # This will be needed later for when we track the torso's rotation
  # We'll leave this as zero for now, it will be set later
  lower_torso_length = 0
  is_first_frame = True

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

    if world_landmarks:
      # Save the length of the lower part of the person's torso on the first frame where someone is detected
      # We'll assume that the person started in a neutral position, facing the directly towards the camera
      if is_first_frame:
        lower_torso_length = PoseMath.get_2d_landmark_distance(world_landmarks, 23, 24)
        is_first_frame = False
      # Printing some messages on the screen for logging purposes
      # Checking if hands are closed or open
      # This may seem weird (LEFT is mapped to Right, while RIGHT is mapped to Left) but they are inverted (for some reason)
      left_hand = "closed" if PoseTracker.is_hand_grabbing(frame, 'Right') else "open"
      right_hand = "closed" if PoseTracker.is_hand_grabbing(frame, 'Left') else "open"
      text = f"LEFT HAND: {left_hand}, RIGHT HAND: {right_hand}"
      processed_frame = cv2.putText(processed_frame, text, (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # Display the current frame image after it has been processed
    cv2.imshow("Pose Tracking", processed_frame)

    # Exit the program if the Q key is pressed
    if cv2.waitKey(1) == ord("q"):
      print("Q key was pressed, exiting the program.")
      break

  # Release the capture and close the window once the program is finished
  capture.release()
  cv2.destroyAllWindows()
