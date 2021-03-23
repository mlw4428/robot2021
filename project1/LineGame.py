import time
import robolib
import robolib.Robot as Robot
import sys
from sys import stdout
import RPi.GPIO as myLineSensor
from datetime import datetime
import logging as sessionLog


sessionLogFilename = datetime.now().strftime('LineGame_%H_%M_%d_%m_%Y.log')
sessionLog.basicConfig(filename=sessionLogFilename,level=sessionLog.INFO,format=("ROBITLOG:" + '%(asctime)s - %(name)s - %(message)s'))
#sessionRemoteLogger.setLevel(level=sessionLog.INFO)
#sessionRemoteLoggerIP = '127.0.0.1'
#sessionRemoteLoggerPort = 5124


#Robit wheel speed
DRIVE_LEFT_TRIM   = 0
DRIVE_RIGHT_TRIM  = 0
DRIVE_TURN_SPEED = 50
DRIVE_NORM_SPEED = 100
DRIVE_SLOW_SPEED = 50
DRIVE_INTERVAL = .5 # How long we drive until we check again


# Line sensors
_LEFTSENSORGPIOVALUE = 7 # maps to 4 on HAT
_RIGHTSENSORGPIOVALUE = 18 # maps to 24 on HAT
myLineSensor.setmode(myLineSensor.BOARD)
myLineSensor.setup(_LEFTSENSORGPIOVALUE, myLineSensor.IN)
myLineSensor.setup(_RIGHTSENSORGPIOVALUE, myLineSensor.IN)

sessionLog.info("****** DEFAULT VALUES ******")
sessionLog.info("MOTOR CONFIG")
sessionLog.info("------------")
sessionLog.info('LEFT TRIM = '+ str(DRIVE_LEFT_TRIM) + '     RIGHT TRIM = ' + str(DRIVE_RIGHT_TRIM)) #record starting trim levels in log
sessionLog.info ('TURN SPEED = '+ str(DRIVE_TURN_SPEED) + '     NORMAL SPEED = ' + str(DRIVE_NORM_SPEED) + '     SLOW SPEED = ' + str(DRIVE_SLOW_SPEED))
sessionLog.info("SENSOR CONFIG")
sessionLog.info("-------------")
sessionLog.info ("LEFT SENSOR IS MAPPED TO PIN: "+ str(_LEFTSENSORGPIOVALUE))
sessionLog.info ("RIGHT SENSOR IS MAPPED TO PIN : "+ str(_RIGHTSENSORGPIOVALUE))
sessionLog.info("")
myRobot = Robot.Robot(left_trim=DRIVE_LEFT_TRIM,right_trim=DRIVE_RIGHT_TRIM,left_id=1,right_id=4)

class LineGame:
    """ Class that plays the Line Game - following a black line on a white board """
    
def eBrake(): #for future use
      sessionLog.error(" ** !!! EMERGENCY BRAKE HAS BEEN DEPLOYED !!! **")
      myRobot.stop()
def InitTest(testSpeed = 50, testTime = .5): #tests wheels/calibration
    sessionLog.debug('*** Motor Testing Starting ***')
    sessionLog.debug('TEST MOTOR SPEED: ' + str(testSpeed))
    sessionLog.debug('TEST MOTOR RUNTIME: ' + str(testTime))
    myRobot.forward(testSpeed,testTime)
    myRobot.backward(testSpeed,testTime)
    myRobot.left(testSpeed,testTime)
    myRobot.right(testSpeed,testTime)
def checkSensorLeft(): 
    myleftsensorvalue = myLineSensor.input(_LEFTSENSORGPIOVALUE)
    sessionLog.info("LEFT SENSOR VALUE: " + str(myleftsensorvalue))
    return myleftsensorvalue
def checkSensorRight():
    myrightsensorvalue = myLineSensor.input(_RIGHTSENSORGPIOVALUE)
    sessionLog.info("MY RIGHT SENSOR VALUE: " + str(myrightsensorvalue))
    return myrightsensorvalue
    print("")
def sensorDriveValue(followLineMode = True): 
    '''Determines the direction the robot needs to travel based upon the output of the line sensors.
    
    Optional parameter: avoidLineMode
        - This parameter switches the robot from a "follow the line" to "regard the line as a barrier" 

    Returns int drivevalue
        -1 = Unknown/Stop, this is the default option for the safety of the robot
        0 = go straight
        1 = turn left
        2 = turn right
        
    
    '''
    drivevalue = -1 #default return value to stop for safety
    if checkSensorLeft() == 1 and checkSensorRight() == 0: # Line is seen on the left sensor, but not the right
        drivevalue = 2
    elif checkSensorLeft() == 0 and checkSensorRight() == 1: # Line is seen on the right sensor, but not the left
            drivevalue = 1
    elif checkSensorLeft() == 1 and checkSensorRight() == 1: # Line is seen on both sides of the sensor
                drivevalue = 0
    elif checkSensorLeft() == 0 and checkSensorRight() == 0: #Line isn't seen anywhere
            drivevalue = 1 # Just turn left and we'll just keep turning until we get both sensors on OR off the tracking or we spin in place safely
    else: #If we get here our logic up above didn't cover something, so stop the bot
            drivevalue = -1
    if followLineMode == True and drivevalue == 1:
        drivevalue = 2
    if followLineMode == True and drivevalue == 2:
        drivevalue = 1
    return drivevalue
def start_game(doTest = False, justDoStop = False, doRemoteLogging=False, remoteLogIP="", remoteLogPort=0, DRIVE_SPEED = DRIVE_NORM_SPEED, DRIVE_TURN = DRIVE_TURN_SPEED, driveSession = 86400):
    ''' Starts the game. If doTest = true an inital motor test will occur
    
    PARAMETERS:
    doTest = Tests servos are working by moving the robot forward, backward, and turning left and then right
    justDoStop = Meant for developer use, if you stop running a python program via debugger, sometimes servos get stuck "on", this issues a stop motor to both wheels
    driveSession = # of seconds we will drive for, default and maximu is 24 hours and minimum is 1 second
    
    '''
    if justDoStop == True:
        eBrake()
        sys.exit()
    if driveSession < 1:
        driveSession == 1
    elif driveSession > 86400:
        driveSession == 86400
    else: 
        driveSession == 86400
    sessionLog.info('start_game - starting game')
   #if doRemoteLogging: #if we're doing remote logging
        #if len(remoteLogIP) > 0: sessionRemoteLoggerIP 
       # sessionRemoteLogger = sessionLog.handlers.SysLogHandler(address=(sessionRemoteLoggerIP,sessionRemoteLoggerPort))
       # session.Logging.addHandler(sessionRemoteLogger)'''
    if (doTest == True): 
        sessionLog.info("Doing preliminary motor testing")
        InitTest()
    print("** DRIVING ** - ")
    startGameTime = time.time()
    gameLooping = True
    while gameLooping is True:
        if (time.time() - startGameTime > driveSession):
            break # if > driveSession then break
        checkThisDriveValue = sensorDriveValue()
        sessionLog.info('SensorDriveValue: '+ str(sensorDriveValue()))
        if checkThisDriveValue == 0: 
            sessionLog.info("FORWARD @ " + str(DRIVE_SPEED) + "FOR " + str(DRIVE_INTERVAL))
            myRobot.forward(DRIVE_SPEED,DRIVE_INTERVAL)
            eBrake()
        elif checkThisDriveValue == 1:
            sessionLog.info("TURN LEFT @ " + str(DRIVE_TURN) + "FOR " + str(DRIVE_INTERVAL))
            myRobot.left(DRIVE_TURN, DRIVE_INTERVAL)
            eBrake()
        elif checkThisDriveValue == 2:
            sessionLog.info("TURN RIGHT @ " + str(DRIVE_TURN) + "FOR " + str(DRIVE_INTERVAL))
            myRobot.right(DRIVE_TURN, DRIVE_INTERVAL)
            eBrake()
        elif checkThisDriveValue == -1:
            eBrake()
        else: # If we get here something is wrong
            sessionLog.exception("DRIVE LOGIC RESULT ERROR. DRIVE LOGIC RETURNED: " + str(checkThisDriveValue))
            eBrake()
            sys.exit(1)
    sys.exit(0)
start_game(doTest=False,justDoStop=True)
