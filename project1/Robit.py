#Robit

from os import system, name 
from time import sleep
import robolib.LineGame as roboLineGame
import robolib.SessionLogger as roboLog
isInit = False

def clear():  #Clears screen for Windows or MacOS/Linux - other OSes will try to use clear command and may not work...you'll need to deal with that somehow
       # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 



def initRobit():
    print("Matt Wilson's Ro-Bit version 1.0 (c) 2021 Matt Wilson")
    print("This software is licensed under public domain except for code licensed under GPL which shall remain under its own license")
    print("Initializing Ro-bit")

# #This is the follow the line mode, which will drive the robot forward/backward and make turns following a line using the light sensors on the front of chassis 
def followTheLineMode():
    print(" ")
# Main program loop
def main():
    if (isInit == False): 
        print ("") 
        #initRobit()
    #Robot.Robot.stop
    menu = None
    while menu is None:
        try:
            roboLog.debug("Building menu")
            print("**************************")
            print("*         RO-BIT         *")
            print("* Created by Matt Wilson *  ")
            print("**************************")
            print (" ")
            print ("Select a running mode")
            print ("1) Follow the line - no init")
            print ("2) Not Implemented")
            print ("")1
            print ("")
            print ("Entering 0 exits the program")
            dirty_input = raw_input()
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
        roboLineGame.start_game(doTest = False, justDoStop = False, driveSession = 10)
    elif menu == 0:
        exit
    else:
        clear()
        print("What you entered is not a valid menu selection, please try again.")
        main()
 
 # Start program and call main
if __name__ == "__main__":
    print ("Ro-bit starting...")
    clear()
    main()