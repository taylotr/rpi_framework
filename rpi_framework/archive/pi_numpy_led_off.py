#! /usr/bin/python

# Import necessary modules
import time, os, numpy

# Variable Declaration
led_file = '/dev/pi-blaster'


led_file_out = os.open(led_file, os.O_WRONLY | os.O_NONBLOCK)

timer_interval = 0.001

led_reverse_pistepper_start = 0.000
led_reverse_pistepper_stop = 0.05
led_reverse_pistepper_step = 0.001

led_pitimer_while_loop_count = 1
testnupy = numpy.arange(led_reverse_pistepper_start, led_reverse_pistepper_stop, led_reverse_pistepper_step)
#testnupy = [numpy.arange(led_reverse_pistepper_start, led_reverse_pistepper_stop, led_reverse_pistepper_step)]



# Define Subroutine
def pistepper(): # Incremental stepper for the LEDs.
	for i in testnupy: 
#		os.write(led_file_out, '2=' + str(i) + '\n')
		os.write(led_file_out, '2=' + str(i) + '\n')
		print i
		piwait()


def reversed_pistepper(): # Decremental stepper for the LEDs.
	for i in reversed(testnupy): 
		os.write(led_file_out, '2=' + str(i) + '\n')
#		os.write(led_file_out, "\n" .join(map(lambda i: str(i), testnupy)) + "\n")
#	os.write(led_file_out, '\n2=' .join(str(i) for i in  reversed(testnupy)) + '\n')
#	os.write(led_file_out, 'EOF')
	print i
	piwait()


def piwait(): # This is a "wait" timer, that we can call in other subroutines if we want.
	time.sleep(timer_interval)


def picleanup():
	print "picleanup running"
#	os.write(led_file_out, 'EOF\n')
	print "EOF\n"
	os.close(led_file_out) # Close the file handle when complete.
	



# Call Subroutine
#pistepper()
reversed_pistepper()
picleanup()

# Closeout
