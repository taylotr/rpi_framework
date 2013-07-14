#! /usr/bin/python

# Import necessary modules
import time, os

# Variable Declaration
led_file = "/dev/pi-blaster"
led_file_out = os.open( led_file, os.O_WRONLY|os.O_NONBLOCK )

timer_interval = 0.006

led_pistepper_start = 0.0
led_pistepper_stop = 0.6
led_pistepper_step = 0.001

led_pitimer_while_loop_count = 1



# Define Subroutine
def pistepper(start, stop, step): # Incremental stepper for the LEDs.
	r = start
	while r <= stop:
		yield r
		os.write(led_file_out, '2=' + str(r) + '\n')
		piwait()
		r += step

def pitimer(): # This is the timer for the steppers, it is the primary subroutine for the steppers.
	count = 0
	while (count < led_pitimer_while_loop_count):
		i0=pistepper(led_pistepper_start, led_pistepper_stop, led_pistepper_step)
		["%g" % x for x in i0]

		count = count + 1

def piwait(): # This is a "wait" timer, that we can call in other subroutines if we want.
	time.sleep(timer_interval)


def picleanup():
	# Added two "0" writes, as the LED's were turning off completely.
	os.write(led_file_out, '2=0.6' + '\n')
	os.write(led_file_out, '2=0.6' + '\n')
	os.write(led_file_out, '2=0.6' + '\n')



# Call Subroutine
pitimer()
picleanup()

# Closeout
os.close(led_file_out) # Close the file handle when complete.
