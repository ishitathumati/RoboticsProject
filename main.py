import interface
import time

buttonPressed = True
go = False
IRdetected = False;
counter = 0
interface.connect()
interface.stop()
time.sleep(2)
interface.start()
time.sleep(2)
interface.passive()
time.sleep(2)
interface.full()
time.sleep(2)

#write the song
interface.writeSong()

while buttonPressed == True:
    time.sleep(.25)
    if interface.buttonRead() == 1:
        go = True
        buttonPressed = False
        break

time.sleep(0.25)

while go == True:
    interface.drive()
    while True:
        button = interface.isPressed()
        bump_wheel = interface.WaB_Check()
        distR = interface.distanceFromWallR()
        distFCR = (interface.distanceFromWallFR() + interface.distanceFromWallCR()) * 0.5
        uTR = interface.PDR(distR)

        IROmni = interface.irSenseOmni();
        IRLeft = interface.irSenseLeft();
        IRRight = interface.irSenseRight();

        if (IRLeft != 0) and (IRRight != 0):
            IRdetected = True;

        if button == 1: #From the is Pressed method: if the robot was stopped and the button was pressed it'll start moving again
            interface.drive()
        elif button == 0: #From the is Pressed method: if the robot was moving and the button was pressed it'll stop
            interface.drive0()

        if interface.move == True:
            if IRdetected == True:

                if interface.currentSense() > 0 or interface.chargeSense() != 0: #if roomba is on the dock
                    interface.drive0()
                    interface.playSong()
                    time.sleep(3)
                    interface.quit()

                if (((bump_wheel[0] == True) or (bump_wheel[1] == True)) and (((IRLeft != 0) and (IROmni != 0)) or ((IRRight != 0) and (IROmni != 0)))): # left or right bumper hits Dock
                    if counter == 0:
                        interface.driveReverse()
                        time.sleep(1)
                        interface.driveSlowly()
                        time.sleep(3.2)
                        interface.drive0()
                        counter = 1
                    else:
                        interface.drive0()
                        interface.playSong()
                        time.sleep(3)
                        interface.quit()

                elif(((IRLeft == 161) and (IRRight == 161)) or ((IRLeft == 172) and (IRRight == 172)) or ((IRLeft == 173) and (IRRight == 173))
                or ((IRLeft == 173) and (IRRight == 0)) or ((IRLeft == 0) and (IRRight == 173))):
                    interface.driveSlowly()
                    time.sleep(2.5)
                    #1 Drive Straight Slowly

                elif (IRLeft == 164) or (IRLeft == 168):
                    interface.sDriveLeft()
                    time.sleep(0.0125)
#                    interface.drive0()
                    #2 Very Slight Turn Left

                elif (IRRight == 168) or (IRRight == 164):
                    interface.sDriveRight()
                    time.sleep(0.0125)
#                    interface.drive0()
                    #3 Very Slight Turn Right

                elif (IRLeft == 0) and (IRRight == 0) and (IROmni != 0):
                    interface.driveReverse()
                    time.sleep(interface.rotateJitterhelp())
                    interface.drive0()
                    #13 Stop and Rotate in place until another case is read

            else:
                if bump_wheel[0] == True: #right bumper
                    interface.drive0()
                    interface.rotateLeft()
                    time.sleep(2 * interface.rotate90help())
                    interface.drive0()
                    interface.drive()
                elif bump_wheel[1] == True: #left bumper and both bumpers
                    interface.drive0()
                    interface.rotateRight()
                    time.sleep(2 * interface.rotate90help())
                    interface.drive0()
                    interface.drive()
                elif distFCR > 10: #if approaching wall in front, turn 90 degrees
                    interface.rotateLeft()
                    time.sleep(interface.rotate90help())
                else: #Do normal path correcting
                    interface.driveCorrectR(uTR)

'''
                    Use packet ID:52 (The left IR sensor) and packet ID:53 (The right IR sensor) to balance
                    out the seeking

                    Ignore this{
                    (The robot will be following a wall on its right side originally so the left sensor should orignally pick up more than the
                    right sensor, if the right sensor picks up more than the left that means the robot is turned too far left)
                    (I believe that if the two sensors have EQUAL readings, the roomba is aimed directly at the dock)
                    (there should be a certain minimum distance from the dock that we would want to be completely facing the dock)
                    (if it is further than that distance it can turn more gradually, but if it is under the minimum the robot will have to stop
                    and rotate till its facing directly at the dock)
                    }

                    OKAY this under part is true
                    (there's also the thought: the dock sends out two different kinds of IR, one is read as a green buoy and one is read as
                    a red buoy)
                    (the left sensor should pick up the green buoy first and then the red and once it is picking up both at the same time, that's
                    when it really knows it has to turn)
                    (if the left sensor is just picking up the red buoy IR the robot has gone too far past the Dock and would have to stop and
                    rotate so that the robot is facing at the dock, but it would be on the right side of the dock)


                    ( OKAY All three IR sensors read both colors and the force field)
                    (If they don't read distance at all they just read whether the IR signal is the green or red buoy or both)
                    (This would mean that if both of the left and right sensors of the robot are reading both the green and red sensors it is
                    facing directly at the dock)

                    Roomba 600 Drive on charger
                    The sensor datas that are recievable are:
                    164 - Just the Green Buoy
                    168 - Just the Red Buoy
                    161 - Just the Force field  (this would mean
                            that the robot is pretty off the target
                            like behind the dock or something)

                    172 - Green and Red Buoy
                    165 - Just the Green Buoy and the Force field
                    169 - Just the Red buoy and the force field

                    173 - It's picking up all three IRs - the Green, Red, and Force field
                     (This probably means that the roomba is right infront of the dock)
                     (and we should have it inch forward until it
                     connects with the charger)

                    if (leftIR == GreenAndRed) and (RightIR == GreenAndRed)
                        interface.drive() #Drive Straight because it is facing directly at the sensor

                    Wall follow --> Docking/Button Checking
                    If the IR is detected set into dock mode
                    in dock mode the robot only has to seek the dock and check for the button
'''
