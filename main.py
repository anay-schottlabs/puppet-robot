from pose_tools import PoseTracker, PoseVisualizer, PoseMath
import cv2

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
  frame = cv2.resize(frame, (800, 800))

  # Extract pose data from the current frame
  image_landmarks, world_landmarks = PoseTracker.get_pose_from_image(frame)
  processed_frame = PoseVisualizer.show_pose(frame, image_landmarks)

  right_arm_angle = PoseMath.get_joint_angle(
    world_landmarks.landmark[12],
    world_landmarks.landmark[14]
  )

  processed_frame = cv2.putText(
    processed_frame,
    f"RIGHT SHOULDER: {right_arm_angle}",
    (50, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 0, 0),
    2
  )

  # Display the current frame image after it has been processed
  cv2.imshow("Pose Tracking", processed_frame)

  # Exit the program if the Q key is pressed
  if cv2.waitKey(1) == ord("q"):
    print("Q key was pressed, exiting the program.")
    break

# Release the capture and close the window once the program is finished
capture.release()
cv2.destroyAllWindows()
