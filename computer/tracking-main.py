from pose_tools import PoseTracker, PoseVisualizer, PoseMath
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

    if world_landmarks:
      # This may seem weird (LEFT is mapped to Right, while RIGHT is mapped to Left) but they are inverted (for some reason)
      text = f"LEFT: {PoseTracker.is_hand_grabbing(frame, 'Right')}, RIGHT: {PoseTracker.is_hand_grabbing(frame, 'Left')}"
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
