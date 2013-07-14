#! /usr/bin/python

# Import necessary modules
import time, os, re

# Variable Declaration
global led_file
led_file = '/dev/pi-blaster'


#led_file_out = os.open(led_file, os.O_WRONLY | os.O_NONBLOCK)

timer_interval = 0.01

led_reverse_pistepper_start = 0.6
led_reverse_pistepper_stop = 0.000
led_reverse_pistepper_step = 0.001

led_pitimer_while_loop_count = 1



# Define Subroutine
def reverse_pistepper(start, stop, step): # Decremental stepper for the LEDs.
	r = start
	while r >= stop:
		yield r
		led_file_out = os.open(led_file, os.O_WRONLY | os.O_NONBLOCK)
		os.write(led_file_out, '2=' + str(r) + '\n')
		os.close(led_file_out) # Close the file handle when complete.
		piwait()
		r -= step


def pitimer(): # This is the timer for the steppers, it is the primary subroutine for the steppers.
	count = 0
	while (count < led_pitimer_while_loop_count):
		i0=reverse_pistepper(led_reverse_pistepper_start, led_reverse_pistepper_stop, led_reverse_pistepper_step)
		["%g" % x for x in i0]
		count = count + 1



def piwait(): # This is a "wait" timer, that we can call in other subroutines if we want.
	time.sleep(timer_interval)


def picleanup():
	led_file_out = os.open( led_file, os.O_WRONLY | os.O_NONBLOCK )
	os.write(led_file_out, '2=0' + '\n')
	os.close(led_file_out) # Close the file handle when complete.
	



# Call Subroutine
pitimer()
picleanup()

# Closeout
