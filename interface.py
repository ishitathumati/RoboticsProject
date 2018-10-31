import math
import random
import serial
import time
import struct
import sys

#Global variables
connection = None
move = True

#Takes in chr and sends command to the robot
def sendCommandRaw(command):
    global connection

    try:
        if connection is not None:
            connection.write(chr(command))
            time.sleep(0.1)
        else:
            print "Not connected!"
    except serial.SerialException:
            print "Connection lost!"
            connection = None

#Sends command to the robot
def sendCommand(command):
    global connection

    try:
        if connection is not None:
            connection.write(command)
            time.sleep(0.1)
        else:
            print "Not connected!"
    except serial.SerialException:
            print "Connection has been lost!"
            connection = None

#Reads data from the robot through the sensors
def read():
    global connection

    try:
        connection.write(chr(142) + chr(18))
        time.sleep(0.0125)
        return struct.unpack("b", connection.read(1))[0]
    except serial.SerialException:
        print "Lost connection"
        connection = None
    except struct.error:
        print "Wrong data."
        return None

#Connect to the robot
def connect():
    global connection
    try:
        connection = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        print "Connected"
    except serial.SerialException:
        print "Connection failed"

#Quits the program
def quit():
    sys.exit()

#Starts the OI
def start():
    print 'Start robot'
    sendCommandRaw(128)
    time.sleep(0.25)

#Puts the robot in passive mode
def passive():
    print 'Passive mode'
    sendCommandRaw(128)
    time.sleep(0.25)

#Restarts the robot
def reset():
    print 'Reset robot'
    sendCommandRaw(7)
    time.sleep(0.2)

#Stop the OI
def stop():
    print 'Stop robot'
    sendCommandRaw(173)

#Put the robot in safe mode
def safe():
    print 'Safe mode'
    sendCommandRaw(131)
    time.sleep(0.0125)

#Put the robot in full mode (can be dangerous if not properly controlled)
def full():
    print 'Full mode'
    sendCommandRaw(132)
    time.sleep(0.0125)

#32767 is a special case for the radius for driving straight
def drive():
    print 'Drive robot'
    cmd = struct.pack('!Bhh', 137, 100, 32767)
    sendCommand(cmd)

def driveSlowly():
    cmd = struct.pack('!Bhh', 137, 20, 32767)
    sendCommand(cmd)

def driveReverse():
    cmd = struct.pack('!Bhh', 137, -100, 32767)
    sendCommand(cmd)

#Stop the robot by setting velocity to 0
def drive0():
    print 'Setting velocity to 0'
    cmd = struct.pack('!Bhh', 137, 0, 0)
    sendCommand(cmd)

#check each of the 4 cliffs
def edgeCheck():
    sendCommand(chr(142) + chr(9))
    value = connection.read(1)
    byteL = struct.unpack('b', value)[0]
    sendCommand(chr(142) + chr(10))
    value = connection.read(1)
    byteFL = struct.unpack('b', value)[0]
    sendCommand(chr(142) + chr(11))
    value = connection.read(1)
    byteFR = struct.unpack('b', value)[0]
    sendCommand(chr(142) + chr(12))
    value = connection.read(1)
    byteR = struct.unpack('b', value)[0]
    array = [byteL, byteFL, byteFR, byteR]
    edgesMissing = 0
    for x in range(0, 4):
        edgesMissing += array[x]
#    print "Cliffs present: "
#    print edgesMissing
    return edgesMissing

#wheel drop and bumper check
def WaB_Check():
    sendCommand(chr(142) + chr(7))
    value = connection.read(1)
    time.sleep(0.0125)
    byte = struct.unpack('B', value)[0]
    wDrop = False
    if bool(byte & 0x04) or (byte & 0x08):
        wDrop = True
    bumpL = bool(byte & 0x02)
    bumpR = bool(byte & 0x01)
#    print "Bumper right: "
#    print bumpR
#    print "Bumper left: "
#    print bumpL
#    print "Wheel drop: "
#    print wDrop
    arr = [bumpR, bumpL, wDrop]
    return (arr)

#indefinitely rotates left
def rotateLeft():
#    cmd = struct.pack('!Bhh', 137, -60, 0) #drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, 80, -80) #direct drive
    sendCommand(cmd)

def rotateLeftSlow():
#    cmd = struct.pack('!Bhh', 137, -60, 0) #drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, 30, -30) #direct drive
    sendCommand(cmd)

def sDriveLeft():
#    cmd = struct.pack('!Bhh', 137, -60, 0) #drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, 80, 65) #direct drive
    sendCommand(cmd)

def cDriveLeft():
#    cmd = struct.pack('!Bhh', 137, -60, 0) #drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, 45, 80) #direct drive
    sendCommand(cmd)

#indefinitely rotates right
def rotateRight():
#    cmd = struct.pack('!Bhh', 137, -60, 0)#drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, -80, 80) #direct drive
    sendCommand(cmd)

def rotateRightSlow():
#    cmd = struct.pack('!Bhh', 137, -60, 0)#drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, -30, 30) #direct drive
    sendCommand(cmd)

def sDriveRight():
#    cmd = struct.pack('!Bhh', 137, -60, 0) #drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, 65, 80) #direct drive
    sendCommand(cmd)

def cDriveRight():
#    cmd = struct.pack('!Bhh', 137, -60, 0) #drive
#    sendCommand(cmd)
#    time.sleep(0.6)
#    drive0()
    cmd = struct.pack('!Bhh', 145, 45, 80) #direct drive
    sendCommand(cmd)

#Helper method to pass in data to turn 90 degrees,
#eventually stopping the rotate
def rotate90help():
    return 1.915

def rotate30help():
    return 0.6383333

def rotateJitterhelp():
    return random.uniform(0, 0.213)

#Read in 2 bytes, find the angle between present and last measurement
#Create 2 and Roomba firmware versions 3.4.0 and earlier return an incorrect
#value for angle measured in degrees.
#The value returned must be divided by 0.324056 to get degrees.
def findAngle():
    cmd = struct.pack('!bb', 142, 20)
    sendCommand(cmd)
    value = connection.read(1)
    return (struct.unpack('!b', value)[0])/(0.324056)

#Shows button presses on the robot
#If multiple are pressed it will add their values together
def buttonRead():
    sendCommand(chr(142) + chr(18))
    time.sleep(0.0125)
    value = connection.read(1)
    time.sleep(0.0125)
    byte = struct.unpack('b', value)[0]
    print "Button: "
    print byte
    return byte

#Method to detect button presses, functinality called in main
#When moving, stop the robot
#When stopped, make the robot move
def isPressed():
    global move
    if move == True:
        if (buttonRead() == 1):
            move = False
            return 0
            #^This means the robot should no longer be moving
    if move == False:
        if (buttonRead() == 1):
            move = True
            return 1
            #^This means the robot should be moving

#write the song
def writeSong():
    cmd = struct.pack('!BBBBBBBBBBBBBBBBBBBBB', 140, 0, 9, 55, 64, 48, 64, 51, 16, 53, 16,
                                                  55, 64, 48, 64, 51, 16, 53, 16, 50, 64)
    connection.write(cmd)

#Play a song previously created
def playSong():
    print 'Playing song'
    cmd = struct.pack('!BB', 141, 0)
    connection.write(cmd)

#sense the wall with light bumper, right
#This measures the how far away the wall is
#by measuring the strength of the light recieved
def distanceFromWallR():
    cmd = struct.pack('!BB',142,51)
    sendCommand(cmd)
    value = connection.read(2)
    time.sleep(.0125)
    byte = struct.unpack('>H', value)[0]
    b = math.sqrt(byte)
#    print b
    return b

#sense the wall with light bumper, front right
#This measures the how far away the wall is
#by measuring the strength of the light recieved
def distanceFromWallFR():
    cmd = struct.pack('!BB',142,50)
    sendCommand(cmd)
    value = connection.read(2)
    time.sleep(.0125)
    byte = struct.unpack('>H', value)[0]
    b = math.sqrt(byte)
#    print b
    return b
#sense the wall with light bumper, center right
#This measures the how far away the wall is
#by measuring the strength of the light recieved
def distanceFromWallCR():
    cmd = struct.pack('!BB',142,49)
    sendCommand(cmd)
    value = connection.read(2)
    time.sleep(.0125)
    byte = struct.unpack('>H', value)[0]
    b = math.sqrt(byte)
#    print b
    return b

#This is our PD controller method. It takes the distance from the wall
#as well as what the past distance was when calculating the next change in direction
prevR=0
currR=0
def PDR(distR):
    global prevR
    global currR
    currR = distR
    t = 5 #Dt = .2
    dCurrR = currR - 8
    uTR = 1*(dCurrR) + .2*(dCurrR-prevR)*t
    prevR = dCurrR
#    print uTR
    return uTR

#This takes the output from the PD controller
#to change the direct drive and change the direction of movement
#use the gain to alter wheel velocities accordingly to seek set point
def driveCorrectR(x):
 #If the wall is ending the output from the PD controller
#is multiplied so that the robot takes a sharper turn
    distanceFCR = (distanceFromWallFR() + distanceFromWallCR()) #front and center light bumper readings
    if distanceFCR == 0:
        x = x*1.5
    if x < 7:
        x = x*2
#Turns left or right based on the output from PD
    if x != 0:
        cmd = struct.pack('!Bhh', 145, 40 + x , 40 - x)
#The robot is right on track
    else:
        cmd = struct.pack('!Bhh', 145, 40 , 40)
    sendCommand(cmd)

"""
164 - Just the Green Buoy
168 - Just the Red Buoy
161 - Just the Force field  (this would mean
        that the robot is pretty off the target
        like behind the dock or something)

172 - Green and Red Buoy
165 - Just the Green Buoy and the Force field
169 - Just the Red buoy and the force field

173 - It's picking up all three IRs - the Green, Red, and Force field
"""

def irSenseOmni():
    cmd = struct.pack('!BB', 142, 17)
    connection.write(cmd)
    time.sleep(0.0125)
    value = connection.read(1)
    time.sleep(0.0125)
    byte = struct.unpack('>B', value)[0]
    print "Omni: "
    print byte
    if byte == 164:
        print "Green\n"
    elif byte == 168:
        print "Red\n"
    elif byte == 161:
        print "Force Field\n"
    elif byte == 172:
        print "Green+Red\n"
    elif byte == 165:
        print "Green+ForceField\n"
    elif byte == 169:
        print "Red+ForceField\n"
    elif byte == 173:
        print "Green+Red+ForceField\n"
    return byte

def irSenseLeft():
    cmd = struct.pack('!BB', 142, 52)
    connection.write(cmd)
    time.sleep(0.0125)
    value = connection.read(1)
    time.sleep(0.0125)
    byte = struct.unpack('>B', value)[0]
    print "Left: "
    print byte
    if byte == 164:
        print "Green\n"
    elif byte == 168:
        print "Red\n"
    elif byte == 161:
        print "Force Field\n"
    elif byte == 172:
        print "Green+Red\n"
    elif byte == 165:
        print "Green+ForceField\n"
    elif byte == 169:
        print "Red+ForceField\n"
    elif byte == 173:
        print "Green+Red+ForceField\n"
    return byte

def irSenseRight():
    cmd = struct.pack('!BB', 142, 53)
    connection.write(cmd)
    time.sleep(0.0125)
    value = connection.read(1)
    time.sleep(0.0125)
    byte = struct.unpack('>B', value)[0]
    print "Right: "
    print byte
    if byte == 164:
        print "Green\n"
    elif byte == 168:
        print "Red\n"
    elif byte == 161:
        print "Force Field\n"
    elif byte == 172:
        print "Green+Red\n"
    elif byte == 165:
        print "Green+ForceField\n"
    elif byte == 169:
        print "Red+ForceField\n"
    elif byte == 173:
        print "Green+Red+ForceField\n"
    return byte

def currentSense():
    cmd = struct.pack('!BB', 142, 23)
    connection.write(cmd)
    time.sleep(0.0125)
    value = connection.read(2)
    time.sleep(0.0125)
    byte = struct.unpack('>bb', value)[0]
    print "Current: "
    print byte
    return byte

def chargeSense():
    sendCommand(chr(142) + chr(21))
    time.sleep(0.0125)
    value = connection.read(1)
    time.sleep(0.0125)
    byte = struct.unpack('b', value)[0]
    print "Charge: "
    print byte
    return byte
