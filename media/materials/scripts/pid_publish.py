import cv2

import matplotlib.pyplot as plt

cv2.__version__

import rospy
from geometry_msgs.msg import Twist
from pid_subscribe import image_converter 

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(2)
move = Twist()

move.linear.x = 0.5
move.angular.z = 0.5

while not rospy.is_shutdown():
    pub.publish(move)
    rate.sleep()

from types import FrameType
# Open a video file to read from it:
raw_video = "/content/drive/MyDrive/raw_video_feed.mp4"
video_reader = cv2.VideoCapture(raw_video)
ret, frame = video_reader.read()

# Create a video file to write to:
shape = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video_writer = cv2.VideoWriter('output.mp4', fourcc, 20, (shape[1], shape[0]))

# Beginning a while loop and converting image to grayscale
while ret:
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Iterating through the pixels 
# If the pixel is below 100, we have reached the first point of the line
  firstpoint = 0
  width = 0
  column = 0
  for pixel in gray[219]:
    column = column+1
    if pixel < 100:
       firstpoint = column
       break

#Iterating through the pixel to determine the width of the line
#Incrementing width for every pixel that is below 100
  for pixel in gray[219]:
    if pixel < 100:
      width = width + 1
      break

