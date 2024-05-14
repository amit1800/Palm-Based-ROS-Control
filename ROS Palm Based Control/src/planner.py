import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import Image

def is_yellow(val):
  return val > 100

def plan(left, right):
  command = "STOP"
  if is_yellow(left) and is_yellow(right):
    command = "GO"
  if is_yellow(left) and not is_yellow(right):
    command = "LEFT"
  if not is_yellow(left) and is_yellow(right):
    command = "RIGHT"
  command_publisher.publish(command)
    

def imgCallback(data):
  try:
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    plan(gray_image[700][300], gray_image[700][500])
    gray_image = cv2.line(gray_image, (300,700), (500,700),0,5)
    cv2.imshow("Raw Image", gray_image)
    cv2.waitKey(3)
  except CvBridgeError as e:
    print(e)
bridge = CvBridge()
command_publisher = rospy.Publisher("motor_commands",String)
def main():
  print("Hey Universe!")
  rospy.init_node("myNode")
  img_sub = rospy.Subscriber("/camera/image_raw", Image, imgCallback)
  rospy.spin()

if __name__ == "__main__":
  main()

