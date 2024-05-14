#include <iostream>
#include <string>
#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "std_msgs/String.h"

ros::Publisher frontLeftWheelPub, frontRightWheelPub, backLeftWheelPub, backRightWheelPub;

void commandsCallback(const std_msgs::String::ConstPtr& msg) {
  float leftSpeed = 0;
  float rightSpeed = 0;
  float speed = 2;
  std::string command = msg->data;
  // std::cout << command;
  if(command == "GO") 
  {
    leftSpeed = -2.0;
    rightSpeed = -2.0;
  }
  else if(command == "GO_REALLY_FAST")
  {
    leftSpeed = -4.0; // radians per second
    rightSpeed = -4.0;
  }
  else if(command == "BACK") 
  {
    leftSpeed = 0.5;
    rightSpeed = 0.5;
  } 
  else if(command == "LEFT") 
  {
    leftSpeed = -2.0;
    rightSpeed = -1.0;
  } else if(command == "SHARP_LEFT"){
    leftSpeed = -2.0;
    rightSpeed = 2.0;
  }
  else if(command == "RIGHT") 
  {
    leftSpeed = -1.0;
    rightSpeed = -2.0;
  } else if(command == "SHARP_RIGHT"){
    leftSpeed = 2.0;
    rightSpeed = -2.0;
  }
  else 
  {
    leftSpeed = 0.0;  // Stop the robot
    rightSpeed = 0.0;
  }

  // send messages
  std_msgs::Float64 msgLeft, msgRight;
  msgLeft.data = leftSpeed;
  msgRight.data = rightSpeed;
  frontLeftWheelPub.publish(msgLeft);

  backLeftWheelPub.publish(msgLeft);
  frontRightWheelPub.publish(msgRight);
  backRightWheelPub.publish(msgRight);

}

int main(int argc, char **argv) {
  ros::init(argc, argv, "motorController");
  ros::NodeHandle n;
  ros::Subscriber commandSub = n.subscribe("motor_commands", 1000, commandsCallback);

  frontLeftWheelPub = n.advertise<std_msgs::Float64>("/front_left_wheel_controller/command", 1000);
  frontRightWheelPub = n.advertise<std_msgs::Float64>("/front_right_wheel_controller/command", 1000);
  backLeftWheelPub = n.advertise<std_msgs::Float64>("/back_left_wheel_controller/command", 1000);
  backRightWheelPub = n.advertise<std_msgs::Float64>("/back_right_wheel_controller/command", 1000);
  
  ros::spin();

  return 0;
}
