#Robit

from os import system, name 
from time import sleep
import LineGame

LineGame = LineGame
isInit = False

def clear():  #Clears screen for Windows or MacOS/Linux - other OSes will try to use clear command and may not work...you'll need to deal with that somehow
       # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 



def initRobit():
    print "Matt Wilson's Ro-Bit version 1.0 (c) 2021 Matt Wilson"
    print "This software is licensed under public domain except for code licensed under GPL which shall remain under its own license"
    print "Initializing Ro-bit"

# #This is the follow the line mode, which will drive the robot forward/backward and make turns following a line using the light sensors on the front of chassis 
def followTheLineMode():
    print ''
# Main program loop
def main():
    if (isInit == False): 
        print "" 
        #initRobit()
    #Robot.Robot.stop
    menu = None
    while menu is None:
        try:
            print "**************************"
            print "*         RO-BIT         *"
            print "* Created by Matt Wilson *  "
            print "**************************"
            print ""
            print "Select a running mode"
            print "1) Follow the line"
            print "2) Not Implemented"
            print ""
            print ""
            print "Entering 0 exits the program"
            dirty_input = raw_input("Please enter your selection: ")
            menu = int(dirty_input)
        except ValueError:
            clear()
            print("What you entered is not a valid selection, please try again and enter an integer this time.")      
            continue
        else:
            #age was successfully parsed!
            #we're ready to exit the loop.
            break
    if menu == 1:
        LineGame.LineGame()
    elif menu == 0:
        exit
    else:
        clear()
        print("What you entered is not a valid menu selection, please try again.")
        main()
 
 
 
 # Start program and call main
if __name__ == "__main__":
    print "Ro-bit starting..."
    clear()
    main()



    '''
# Set the trim offset for each motor (left and right).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move the
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -5, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a small
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.
LEFT_TRIM   = 0
RIGHT_TRIM  = 0


# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - left_id: The ID of the left motor, default is 1.
#  - right_id: The ID of the right motor, default is 2.
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Now move the robot around!
# Each call below takes two parameters:
#  - speed: The speed of the movement, a value from 0-255.  The higher the value
#           the faster the movement.  You need to start with a value around 100
#           to get enough torque to move the robot.
#  - time (seconds):  Amount of time to perform the movement.  After moving for
#                     this amount of seconds the robot will stop.  This parameter
#                     is optional and if not specified the robot will start moving
#                     forever.
robot.forward(150, 1.0)   # Move forward at speed 150 for 1 second.
robot.left(200, 0.5)      # Spin left at speed 200 for 0.5 seconds.
robot.forward(150, 1.0)   # Repeat the same movement 3 times below...
robot.left(200, 0.5)
robot.forward(150, 1.0)
robot.left(200, 0.5)
robot.forward(150, 1.0)
robot.right(200, 0.5)

# Spin in place slowly for a few seconds.
robot.right(100)  # No time is specified so the robot will start spinning forever.
time.sleep(2.0)   # Pause for a few seconds while the robot spins (you could do
                  # other processing here though!).
robot.stop()      # Stop the robot from moving.

# Now move backwards and spin right a few times.
robot.backward(150, 1.0)
robot.right(200, 0.5)
robot.backward(150, 1.0)
robot.right(200, 0.5)
robot.backward(150, 1.0)
robot.right(200, 0.5)
robot.backward(150, 1.0)

# That's it!  Note that on exit the robot will automatically stop moving.
    '''