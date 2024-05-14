# Palm-Based-ROS-Control
Project included simulation of a four wheeled ROS robot, which is teleoperated using image processing of a palm, in real time.

Uses Gazebo for simulation of the robot. A dedicated launch file for Gazebo is present.

Robot is made in the form of a URDF file, which is readable by ROS and Gazebo.

Hand tracking is done in Python using the MediaPipe library.

The python node sends teleop commands to another control node written in C++, which finally changes the movement of the URDF content.
