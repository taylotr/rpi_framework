#! /usr/bin/python

# Import necessary modules
import time, os

# Variable Declaration
led_file = "/dev/pi-blaster"
led_file_access_mode = `os.O_WRONLY|os.O_NONBLOCK`
led_file_out = os.open( led_file, os.O_WRONLY|os.O_NONBLOCK )

timer_interval = 0.005

led_pistepper_start = 0.0
led_pistepper_stop = 0.8
led_pistepper_step = 0.001

led_reverse_pistepper_start = 0.8
led_reverse_pistepper_stop = 0.0
led_reverse_pistepper_step = 0.001

led_pitimer_while_loop_count = 1



# Define Subroutine
def pimenu():  # Menu system for test harness.

	ans = True
	while ans:
		print("""
		1. Enable debug and run LED Stepper.
		2. Disable debug and LED Stepper.
		
		Press enter to quit.
		""")
		global pidebug
		ans = raw_input("Welcome to the test harness, please select an option: ")
		if ans == "1":
			print("\n Debug enabled, running harness.")
			pidebug = True
			pitimer()
			picleanup()

		elif ans == "2":
			print("\n Debug disabled, running harness.")
			pidebug = False
			pitimer()
			picleanup()

		elif ans != "":
			print("\n Please select another option, or press enter to exit.")
			picleanup()
	print("\n Exiting, Good-bye!")


def pistepper(start, stop, step): # Incremental stepper for the LEDs.
	r = start
	while r < stop:
		yield r
		os.write(led_file_out, '2=' + str(r) + '\n')
		piwait()
		r += step


def reverse_pistepper(start, stop, step): # Decremental stepper for the LEDs.
	r = start
	while r > stop:
		yield r
		os.write(led_file_out, '2=' + str(r) + '\n')
		piwait()
		r -= step


def pitimer(): # This is the timer for the steppers, it is the primary subroutine for the steppers.
	count = 0
	while (count < led_pitimer_while_loop_count):
		i0=pistepper(led_pistepper_start, led_pistepper_stop, led_pistepper_step)
		["%g" % x for x in i0]

		i0=reverse_pistepper(led_reverse_pistepper_start, led_reverse_pistepper_stop, led_reverse_pistepper_step)
		["%g" % x for x in i0]

		count = count + 1
		if pidebug == True:
			print("\n Step iteration: " +  str(count))


def piwait(): # This is a "wait" timer, that we can call in other subroutines if we want.
	time.sleep(timer_interval)


def picleanup():
	# Added two "0" writes, as the LED's were turning off completely.
	os.write(led_file_out, '2=0' + '\n')
	os.write(led_file_out, '2=0' + '\n')

	# Set the global variable "pidebug, back to False.
	global pidebug
	pidebug = False
	



# Call Subroutine
pimenu()

# Closeout
os.close(led_file_out) # Close the file handle when complete.
