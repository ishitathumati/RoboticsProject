# RoboticsProject
This is a set of python programs that implements basic algorithms for robotic perception, planning, navigation, localization, and manipulation on the mobile robot: iRobot Create 2 Roomba 600. 

## Files: 	
main.py  
interface.py  

## Authors: 
Joseph Basile, Ishita Thumati, Chad Thomas 

### Date:	December 5, 2017

## Descriptions:  
_**interface.py**_: This file imports the serial module, which enables us to connect to the robot. This file also has all the necessary methods which perform tasks like establishing serial connection with the robot, quitting the connection, putting the robot in different modes, sending raw commands to the robot, reading sensor data, driving the robot at a certain velocity and radius and checking for button presses on the robot.This file was further augmented and now includes methods to check if the following sensors are triggered: Left, Right, and Omni IR sensors (packets 17, 52, 53), bumps and wheel drops (packet 7), cliff sensors (packets 9-12), Light Bumper Sensors (packets 49-51). It also includes methods rotate left, rotate right, which are used when robot bumps into an obstacle. Finally, there is also a PD controller and driveCorrectR methods which calculate errors from the robot’s wall sensors and adjust the errors to maintain a given set point and make the robot move parallel to a straight wall.

_**main.py**_: This file imports the interface file and executes most of the methods defined in the interface to make the robot accomplish certain tasks based on some conditions. The methods in the interface are set up and invoked in a logical order of conditions and loops, with timers placed in between changes in states so the robot responds smoothly. 
When the program starts the robot is started up and set in the proper mode. It then listens for a button press from the user. After that point it begins driving forward. While it drives, a loop is running, listening for button presses and reading its bumps and wall sensors. Based on these conditions, the robot responds appropriately with stopping if button is pressed while moving, or adjusting its velocity after PD controller correction and driving parallel to the wall without drifting, turning by 90 degrees if it is approaching a wall in the front. If the infrared sensors pick up a signal, the robot begins seeking the charging dock and adjusts its path as it goes. When the robot reaches the dock, it stops and plays a song.

## File Use:  
1. User is to first connect the robot to the computer using an ethernet cable.  
2. Copy the files to the Raspberry Pi by using scp (IP address of the Raspberry Pi: 192.168.1.1;  
username: pi; password: raspberry).  
3. Connect to the Raspberry Pi by using ssh.   
(ssh pi@192.168.1.1
and input the password).
4. Use command ’screen’ to start a shell window within the ssh session so that the shell is active even through
network disruptions.  
5. Run the files using python interpreter. Start the robot behavior by pressing the clean/power button on the robot 
e.g. python main.py  
6. Unplug the cable from your computer.  

