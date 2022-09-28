#! /usr/bin/env python3
from __future__ import print_function


import rospy
from geometry_msgs.msg import Twist

import roslib
roslib.load_manifest('enph353_ros_lab')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

   
class image_converter:
   
  # Constructor  
  def __init__(self):
    self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
   
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/rrbot/camera1/image_raw",Image,self.callback)

    self.twist = Twist()
  # Function called when a new image is received
  def callback(self,data):
   #convert from ROS image type to OpenCV image type
   try:
     cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
   except CvBridgeError as e:
     print(e)
    
   gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    #finding center of line
   (rows,cols,channels) = cv_image.shape
   firstpoint = 0
   width = 0
   column = 0
   for pixel in gray[rows - 20]:
      column = column+1
      if pixel < 100:
        firstpoint = column
        break
   for pixel in gray[rows - 20]:
      if pixel < 100:
        width = width + 1
        break

   line_pos = (firstpoint+int(width/2))#+30

   cv2.circle(cv_image, (line_pos, rows - 20), 20, (255, 0, 0), -1)
   
    # Figure out if we turn left, right or go forward
    # Create a Twist message that does that.

   center = cols / 2

   self.twist.linear.x = 0.5
   self.twist.angular.z = 0

   if (center+50)<line_pos:
     self.twist.linear.x=0
     self.twist.angular.z = -0.5
   if (center-50) > line_pos:
     self.twist.linear.x = 0
     self.twist.angular.z = 0.5

   self.cmd_pub.publish(self.twist) 


   cv2.imshow("Image window", cv_image)
   cv2.waitKey(3)

   cv2.imshow("Image gray", gray)
   cv2.waitKey(3)
   
def main(args):
  # initialize current script as a ROS node
  rospy.init_node('image_converter', anonymous=True)
  
  # create data processing object
  ic = image_converter()

  # Start ROS event loop and spin until interrupted by keyboard
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

