#!/usr/bin/python
#
# pir_1.py
# Detect movement using a PIR module
#
# Author : Matt Hawkins
# Date   : 21/01/2013

# Import required Python libraries
import RPi.GPIO as GPIO
import time, os, re

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 17

# Path to LED script.
ledOnpath = "/home/pi/rpi_framework/pi_led_on.py"
ledOffpath = "/home/pi/rpi_framework/pi_led_off.py"

ledstatusInPath = "/tmp/led_stepper_status"


print "PIR Module Test (CTRL-C to exit)"

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

#Current_State  = 0
#Previous_State = 0

try:

  print "Waiting for PIR to settle ..."

  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Motion_State  = 0

  print "  Ready."

  # Loop until users quits with CTRL-C
  while True :

    # Read PIR state
    Motion_State = GPIO.input(GPIO_PIR)
    read_ledstatusfile = open(ledstatusInPath, 'r')
    Current_State_Regex = read_ledstatusfile.read()

    Current_State = re.sub(r'2=', "", Current_State_Regex)

    read_ledstatusfile.close()

    if Current_State=='0\n' and Motion_State==1:
      print(Current_State)
      # PIR is triggered
      print "  Motion detected, turning lights on!"

      os.system(ledOnpath)
      print "  Ready."

    elif Current_State=='0.6\n' and Motion_State==1:
      # PIR has returned to ready state
      print(Current_State)
      print "  Motion detected, turning lights off!"

      os.system(ledOffpath)
      print "  Ready."

    elif Current_State<>'0.6\n' and Current_State<>'0\n':
      # PIR has returned to ready state
      print(Current_State)
      print "  Motion detected, turning lights off!"

      os.system(ledOffpath)
      print "  Ready."

    # Wait for 10 milliseconds
    time.sleep(0.01)

except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()
#os.close(ledstatusInPath)
