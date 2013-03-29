#! /usr/bin/python

# Import necessary modules
import time

# Variable Declaration
#led_file = "/home/pi/rpi_framework/pi-blaster.out"
led_file = "/dev/pi-blaster"
led_file_access_mode = "w"
led_file_buffer_size = "0"
led_file_out = open(led_file, led_file_access_mode, 0)

timer_interval = 0.005

led_pistepper_start = 0.0
led_pistepper_stop = 1.0
led_pistepper_step = 0.001

led_reverse_pistepper_start = 1.0
led_reverse_pistepper_stop = 0.0
led_reverse_pistepper_step = 0.001


# Define Subroutine
def pistepper(start, stop, step):
	r = start
	while r < stop:
		yield r
		led_file_out.write('2=' + str(r) + '\n')
		piwait()
		r += step

def reverse_pistepper(start, stop, step):
	r = start
	while r > stop:
		yield r
		led_file_out.write('2=' + str(r) + '\n')
		piwait()
		r -= step

def pitimer():
	count = 0
	while (count < 2):
		i0=pistepper(led_pistepper_start, led_pistepper_stop, led_pistepper_step)
		["%g" % x for x in i0]

		i0=reverse_pistepper(led_reverse_pistepper_start, led_reverse_pistepper_stop, led_reverse_pistepper_step)
		["%g" % x for x in i0]

		count = count + 1

def piwait():
	time.sleep(timer_interval)


# Call Subroutine
pitimer()

# Cleanup
led_file_out.write('2=0' + '\n')
led_file_out.close()
