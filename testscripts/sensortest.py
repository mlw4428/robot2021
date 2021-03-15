# SENSOR DETECTION TEST
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN)

while True:
  i = GPIO.input(7)
  if i == 1:
    print "Movement detected", i
    time.sleep(0.01)
  elif i == 0:
    print "No movement detected", i
    time.sleep(0.01)
