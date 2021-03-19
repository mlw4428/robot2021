import time
import robolib
import robolib.Robot as Robot
import RPi.GPIO as mygpio
from datetime import datetime
import logging as sessionLog

myLeftLineSensor = mygpio
myRightLineSensor = mygpio

sessionLogFormat = "ROBITLOG:" + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
sessionLog.basicConfig(filename=datetime.now().strftime('LineGame_%H_%M_%d_%m_%Y.log'), level=sessionLog.INFO,format=sessionLogFormat) #Basic debug logging

#Robit wheel speed
LEFT_TRIM   = 0
RIGHT_TRIM  = 0
TURN_SPEED = 50
NORM_SPEED = 100
SLOW_SPEED = 50

# Line sensors
_LEFTSENSORGPIOVALUE = 7
_RIGHTSENSORGPIOVALUE = 18
myLeftLineSensor.setwarnings(False)
myLeftLineSensor.setmode(mygpio.BOARD)
myLeftLineSensor.setup(_LEFTSENSORGPIOVALUE ,mygpio.IN) # maps to 4 on HAT
myRightLineSensor.setwarnings(False)
myRightLineSensor.setmode(mygpio.BOARD)
myRightLineSensor.setup(_RIGHTSENSORGPIOVALUE,mygpio.IN) # maps to 24 on HAT


sessionLog.info("****** DEFAULT VALUES ******")
sessionLog.info("MOTOR CONFIG")
sessionLog.info("------------")
sessionLog.info('LEFT TRIM = '+ str(LEFT_TRIM) + '     RIGHT TRIM = ' + str(RIGHT_TRIM)) #record starting trim levels in log
sessionLog.info ('TURN SPEED = '+ str(TURN_SPEED) + '     NORMAL SPEED = ' + str(NORM_SPEED) + '     SLOW SPEED = ' + str(SLOW_SPEED))
sessionLog.info("SENSOR CONFIG")
sessionLog.info("-------------")
sessionLog.info ("LEFT SENSOR IS MAPPED TO PIN: "+ str(_LEFTSENSORGPIOVALUE))
sessionLog.info ("RIGHT SENSOR IS MAPPED TO PIN : "+ str(_RIGHTSENSORGPIOVALUE))

sessionLog.info("")
myRobot = Robot.Robot(left_trim=LEFT_TRIM,right_trim=RIGHT_TRIM,left_id=1,right_id=4)

class LineGame:
    """ Class that plays the Line Game - following a black line on a white board """
    
def eBrake():
  
    myRobot.stop()
def InitTest(): #tests wheels/calibration
    sessionLog.debug('doInit')
    myRobot.forward(50,.50)
    myRobot.backward(50,.5)
    myRobot.left(50,.5)
    myRobot.right(50,.5)
def checkSensorLeft():
    sensorleftvalue = 0
    print("")
def checkSensorRight():
    sensorrightvalue = 0
    print("")
def sensorDriveValue(): 
    drivevalue = 0 #default return value to stop for safety
    """This checks the sensors first left then right.

    Returns a value based on the direction the robot will need to steer
        -1 = UNKNOWN/ERR, default action will be stop
        0 = STOP
        1 = LEFT
        2 = RIGHT"""

    return drivevalue
def start_game(doTest):
    """ Starts the game. If doTest = true an inital motor test will occur"""
    sessionLog.info('start_game - starting game')
    if (doTest == True): 
        sessionLog.info("Doing preliminary testing")
        InitTest()
    print("Starting Line Game")
    sessionLog.info('SensorDriveValue: '+ str(sensorDriveValue()))
    gameLooping = True
    while gameLooping is True:
        sensorDriveValue
start_game(True)
