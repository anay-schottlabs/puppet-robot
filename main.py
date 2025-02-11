from pose_tracker import PoseTracker
import cv2
import mediapipe as mp

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

  # Display the current frame image
  cv2.imshow("Pose Tracking", frame)

  # Exit the program if the Q key is pressed
  if cv2.waitKey(1) == ord("q"):
    break

# Release the capture and close the window once the program is finished
capture.release()
cv2.destroyAllWindows()
