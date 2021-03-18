import time
import robolib
import robolib.Robot as Robot
import RPi.GPIO as mygpio
import logging as sessionLog
from datetime import datetime
class LineGame:
    """ Class that plays the Line Game - following a black line on a white board """
    
def eBrake():
  
    myRobot.stop()
def doInit(): #tests wheels/calibration
    sessionLog.debug('doInit')
    #myRobot.forward(150,3.0)
    #myRobot.backward(150,3.0)
    myRobot.left(150,3.0)
def start_game():
    sessionLog.debug('start_game - starting game')
    doInit()
    print("Starting Line Game")
   

sessionLog.basicConfig(filename=datetime.now().strftime('mylogfile_%H_%M_%d_%m_%Y.log'), level=sessionLog.DEBUG) #Basic debug logging
LEFT_TRIM   = -3
RIGHT_TRIM  = 4
sessionLog.debug('LEFT TRIM = '+ str(LEFT_TRIM) + ' RIGHT TRIM = ' + str(RIGHT_TRIM)) #record starting trim levels in log
myRobot = Robot.Robot(left_trim=LEFT_TRIM,right_trim=RIGHT_TRIM,left_id=1,right_id=2)
start_game()
