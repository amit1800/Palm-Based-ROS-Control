#!/usr/bin/env python
import rospy 
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class RosNode:
    def sendVelocites(self, twist):
        if not twist.linear.x == 0:
            if twist.angular.z > 0:
                self.fl_motor.publish(twist.linear.x + twist.angular.z)
                self.fr_motor.publish(twist.linear.x)
                self.bl_motor.publish(twist.linear.x + twist.angular.z)
                self.br_motor.publish(twist.linear.x)
            elif twist.angular.z < 0:

                self.fl_motor.publish(twist.linear.x)
                self.fr_motor.publish(twist.linear.x - twist.angular.z)
                self.bl_motor.publish(twist.linear.x)
                self.br_motor.publish(twist.linear.x - twist.angular.z)
            else:
                self.fl_motor.publish(twist.linear.x)
                self.fr_motor.publish(twist.linear.x)
                self.bl_motor.publish(twist.linear.x)
                self.br_motor.publish(twist.linear.x)
        else:
            self.fl_motor.publish(0)
            self.fr_motor.publish(0)
            self.bl_motor.publish(0)
            self.br_motor.publish(0)

    def sendVels(self, twist):
        left_vel, right_vel = 0,0
        left_vel = left_vel + twist.linear.x + twist.angular.z
        right_vel = right_vel + twist.linear.x - twist.angular.z
        self.fl_motor.publish(-left_vel)
        self.bl_motor.publish(-left_vel)
        self.fr_motor.publish(-right_vel)
        self.br_motor.publish(-right_vel)
    def callback(self,v):
        print(self.i,v.linear.x)
        self.i = self.i + 1
        self.sendVels(v)
    def __init__(self):
        rospy.init_node("ros_node")
        rospy.loginfo("Starting RosNode.")
        cmd_sub = rospy.Subscriber("/cmd_vel", Twist, self.callback)
        self.fl_motor = rospy.Publisher("/front_left_wheel_controller/command",Float64,queue_size=100)
        self.fr_motor = rospy.Publisher("/front_right_wheel_controller/command",Float64,queue_size=100)
        self.bl_motor = rospy.Publisher("/back_left_wheel_controller/command",Float64,queue_size=100)
        self.br_motor = rospy.Publisher("/back_right_wheel_controller/command",Float64,queue_size=100)
        self.i = 0
        pass


if __name__ == "__main__":
    ros_node = RosNode()
    rospy.spin()