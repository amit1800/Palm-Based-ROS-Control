import cv2
import mediapipe as mp
import time
import rospy
from cv_bridge import CvBridge,CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import Image

bridge = CvBridge()

def imgCallback(data):
  try:
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("Raw Image", cv_image)
    cv2.waitKey(3)
  except CvBridgeError as e:
    print(e)
def main():
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    cTime = 0
    rospy.init_node("handTracker")
    img_sub = rospy.Subscriber("/camera/image_raw", Image, imgCallback)
#   img_sub = rospy.Subscriber("/camera/image_raw", Image, imgCallback)
    command_publisher = rospy.Publisher("motor_commands",String,queue_size=100)
    # rospy.spin()

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            # print(results.multi_hand_landmarks)
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    # if id == 0:
                    #     cv2.circle(img, (cx,cy), 8, (255,0,255), cv2.FILLED)
                diff = handLms.landmark[8].x - handLms.landmark[5].x
                if diff > 0.05:
                    if handLms.landmark[12].y < handLms.landmark[10].y:
                        print("SHARP LEFT")
                        command_publisher.publish("SHARP_LEFT")
                    else:
                        print("LEFT")
                        command_publisher.publish("LEFT")
                elif diff < -0.05:
                    if handLms.landmark[12].y < handLms.landmark[10].y:
                        print("SHARP RIGHT")
                        command_publisher.publish("SHARP_RIGHT")
                    else:
                        print("RIGHT")
                        command_publisher.publish("RIGHT")
                elif handLms.landmark[8].y > handLms.landmark[6].y:
                    print("STOP")
                    command_publisher.publish("STOP")
                else:
                    if handLms.landmark[12].y < handLms.landmark[10].y:
                        print("FAST STRAIGHT")
                        command_publisher.publish("GO_REALLY_FAST")
                    else:
                        print("STRAIGHT")
                        command_publisher.publish("GO")
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # else:
            #     # when hand leaves the screen
            #     command_publisher.publish("STOP")


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

if __name__ == "__main__":
  main()