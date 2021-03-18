import time
import robolib
import robolib.Robot as Robot
import RPi.GPIO as mygpio
from datetime import datetime
import logging as sessionLog

sessionLog.basicConfig(filename=datetime.now().strftime('LineGame_%H_%M_%d_%m_%Y.log'), level=sessionLog.INFO) #Basic debug logging
LEFT_TRIM   = 0
RIGHT_TRIM  = 0
TURN_SPEED = 50
NORM_SPEED = 150
SLOW_SPEED = 75
sessionLog.info("****** DEFAULT VALUES ******")
sessionLog.info('LEFT TRIM = '+ str(LEFT_TRIM) + '     RIGHT TRIM = ' + str(RIGHT_TRIM)) #record starting trim levels in log
sessionLog.info ('TURN SPEED = '+ str(TURN_SPEED) + '     NORMAL SPEED = ' + str(NORM_SPEED) + '     SLOW SPEED = ' + str(SLOW_SPEED))
sessionLog.info("")
myRobot = Robot.Robot(left_trim=LEFT_TRIM,right_trim=RIGHT_TRIM,left_id=1,right_id=4)

class LineGame:
    """ Class that plays the Line Game - following a black line on a white board """
    
def eBrake():
  
    myRobot.stop()
def doInit(): #tests wheels/calibration
    sessionLog.debug('doInit')
    myRobot.forward(100,.50)
    myRobot.backward(100,.5)
    myRobot.left(100,.5)
    myRobot.right(100,.5)
def checkSensorLeft():
    sensorleftvalue = 0
    print("")
def checkSensorRight():
    sensorrightvalue = 0
    print("")
def SensorDriveValue(): 
    drivevalue = 0 #default return value to stop for safety
    """This checks the sensors first left then right.

    Returns a value based on the direction the robot will need to steer
        -1 = UNKNOWN/ERR, default action will be stop
        0 = STOP
        1 = LEFT
        2 = RIGHT"""

    return drivevalue
def start_game():
    """ Starts the game."""
    sessionLog.info('start_game - starting game')
    doInit()
    print("Starting Line Game")
    sessionLog.info('SensorDriveValue: '+ str(SensorDriveValue()))
   
start_game()
