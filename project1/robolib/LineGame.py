import time
import sys
import Robot as Robot
import RPi.GPIO as myLineSensor
import SessionLogger as sessionLog


#Robit wheel speed
DRIVE_LEFT_TRIM   = 0
DRIVE_RIGHT_TRIM  = 0
DRIVE_TURN_SPEED = 100
DRIVE_NORM_SPEED = 75
DRIVE_SLOW_SPEED = 25
DRIVE_INTERVAL = .01 # How long we drive until we check again


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
    sessionLog.debug('MOVE FORWARD')
    myRobot.forward(testSpeed,testTime)
    sessionLog.debug('MOVE BACKWARD')
    myRobot.backward(testSpeed,testTime)
    sessionLog.debug('TURN LEFT')
    myRobot.left(testSpeed,testTime)
    sessionLog.debug('TURN RIGHT')
    myRobot.right(testSpeed,testTime)
def checkSensorLeft(): 
    myleftsensorvalue = myLineSensor.input(_LEFTSENSORGPIOVALUE)
    sessionLog.debug("LEFT SENSOR VALUE: " + str(myleftsensorvalue))
    return myleftsensorvalue
def checkSensorRight():
    myrightsensorvalue = myLineSensor.input(_RIGHTSENSORGPIOVALUE)
    sessionLog.debug("MY RIGHT SENSOR VALUE: " + str(myrightsensorvalue))
    return myrightsensorvalue
    print("")
def sensorDriveValue(followLineMode = True): 
    '''Determines the direction the robot needs to travel based upon the output of the line sensors.
    
    Optional parameter: followLineMode
        - This parameter switches the robot from a "follow the line" to "regard the line as a barrier"
            which has the effect of flipping the drive value for left and right

    Returns int drivevalue which tells our motors to turn left/right, seek a turn, or go straight or stop. If 
       
    
    '''
    drivevalue = -1 #default return value to stop for safety
    if checkSensorLeft() == 0 and checkSensorRight() == 1: # Line is seen on the left sensor, but not the right
        sessionLog.debug("LEFT SENSOR ON, RIGHT SENSOR OFF")
        drivevalue = 2
    elif checkSensorLeft() == 1 and checkSensorRight() == 0: # Line is seen on the right sensor, but not the left
            sessionLog.debug("LEFT SENSOR OFF, RIGHT SENSOR ON")
            drivevalue = 1
    elif checkSensorLeft() == 0 and checkSensorRight() == 0: # Line isn't seen anywhere
                sessionLog.debug("OFF THE LINE") 
                if followLineMode == True 
                    drivevalue = -10
                else 
                    drivevalue = 0
    elif checkSensorLeft() == 1 and checkSensorRight() == 1: # Both sensors are on the line
            sessionLog.debug("ON THE LINE")
                if followLineMode == True 
                    drivevalue = 0
                else 
                    drivevalue = -10
    if followLineMode == False and drivevalue == 1:
        drivevalue = 2
    if followLineMode == False and drivevalue == 2:
        drivevalue = 1
    return drivevalue
def doSearch(lastValue = 0, sessionTime=-1):
    if sessionTime = -1:
        raise Exception("Search called without sessionTime being passed. Exiting as punishment.")
        sessionLog.error("doSearch() called without sessionTime. Exiting program.")
        sys.exit()
    sessionLog.debug("*** FIND TRACK SEARCH MODE STARTED ***")
    keepLooking = True
    lookTime = DRIVE_INTERVAL
    lookSpeed = DRIVE_NORM_SPEED
    lookTimeAdd = .5
    while keepLooking == True:
        if (time.time() - startGameTime > driveSession): #keep us from deadlocking here
                sessionLog.info("*** TRACK SEARCH ENDED DUE TO DRIVE SESSION ENDING ***")
                 break
        if lastSensorValue == 1: #if last sensor value was to turn left, turn right
            sessionLog.info("searching right...")
            myRobot.right(lookSpeed, lookTime)
        if lastSensorValue == 2: #if last sensor value was to turn right, turn left
            sessionLog.info("searching left...")
            myRobot.left(lookSpeed, lookTime)
        sessionLog.info("Searching left..." + str(sensorDriveValue()))
        if sensorDriveValue() > -1:
            keepLooking = False
            break
        myRobot.right(lookSpeed, lookTime)
        sessionLog.debug("Searching right..." + str(sensorDriveValue()))
        if sensorDriveValue() > -1:
            keepLooking = False
            break
        lookTime = lookTime + lookTimeAdd #increase how far we look
        myRobot.right(lookSpeed, lookTime)
        sessionLog.debug("Extending search right... " + str(sensorDriveValue()))
        if sensorDriveValue() > -1:
            keepLooking = False
            break
        myRobot.left(lookSpeed, lookTime * 2) #extend a search further left
        lookTime = lookTime * 2
        sessionLog.debug("Extending search left: " + str(sensorDriveValue()))
        if sensorDriveValue() > -1:
            keepLooking = False
            break
        lookTime = lookTime + lookTimeAdd
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
        InitTest()
    print("** DRIVING ** - ")
    startGameTime = time.time()
    gameLooping = True
    lastSensorValue = 0
    while gameLooping is True:
        if (time.time() - startGameTime > driveSession):
            break # if > driveSession then break
        checkThisDriveValue = sensorDriveValue()
        sessionLog.info('SensorDriveValue: '+ str(sensorDriveValue()))
        if checkThisDriveValue == 0: 
            sessionLog.info("FORWARD @ " + str(DRIVE_SPEED) + "FOR " + str(DRIVE_INTERVAL))
            myRobot.forward(DRIVE_SPEED,DRIVE_INTERVAL)
        elif checkThisDriveValue == 1:
            sessionLog.info("TURN LEFT @ " + str(DRIVE_TURN) + "FOR " + str(DRIVE_INTERVAL))
            myRobot.left(DRIVE_TURN, DRIVE_INTERVAL)
        elif checkThisDriveValue == 2:
            sessionLog.info("TURN RIGHT @ " + str(DRIVE_TURN) + "FOR " + str(DRIVE_INTERVAL))
            myRobot.right(DRIVE_TURN, DRIVE_INTERVAL)
        elif checkThisDriveValue == -10: #find the turn, do this by turning in wider archs left or right
            doSearch(lastValue=lastSensorValue,sessionTime=driveSession)
        elif checkThisDriveValue == -1:
            eBrake()
        else: # If we get here something is wrong
            sessionLog.exception("DRIVE LOGIC RESULT ERROR. DRIVE LOGIC RETURNED: " + str(checkThisDriveValue))
            eBrake()
            sys.exit(1)
        lastSensorValue = checkThisDriveValue
    sys.exit(0)
start_game(doTest=False,justDoStop=False,driveSession=60)
