from pose import Point, Limb, Hand, Pose

class PoseTracker:
  @staticmethod
  def get_pose_from_image(image):
    # process pose, if none is detected end the method and return blank data (also include blank hand data)
    # if the pose exists in the image, extract hands and make up for hidden hands with blank data
    # extract the hand positions as a pose object
    pass
