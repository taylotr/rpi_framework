#!/usr/bin/env python


#      Author - TT
#      Creation Date - 05/09/13
#      Modification Date - 05/09/13
#      Script Name - pi_daemon_blaster.py
#      Description - The intent of this daemon is to monitor the /dev/pi-blaster named pipe.  It writes to a
#			sqlite3 database to retain persistence across reboots.
#      Aditional Authors Notes - 
#		-  05-18-13  Finally performing the notations and comments.
#      Requirements -  
#      Changelog:
#          05/09/13 - Script started.
#      Usage Notes:
#              pi_daemon_blaster.py
#
#           Input parameters:
#              No options at this time, the script is only set to turn the LEDs off.  Will add the
#                      statements later to dim/un-dim.
#
#
#
# Import necessary modules
#	time - Used in the piwait() module for the sleep statement.
#	os - Used for the opening of the named pipe: /dev/pi-blaster.
#	sys - Used in the "MyDaemon()" subroutine as the main body of the daemon.
#	sqlite3 - The internal database used for data persistence across restarts and SIG continuity.
#	re - Regular expressions to match/subsitute for the actual insertion of the data to /dev/pi-blaster.

import sys, time, os, sqlite3, re, signal, threading
import RPi.GPIO as GPIO
from pi_daemon_external import daemon
from threading import Thread


ledstatusOutPath = '/tmp/monitoring_daemon.db'
ledstatusPath = '/tmp/monitoring_daemon.db'
regex_pattern = r'[0-9.]+'

def pimotion():
#	Use BCM GPIO references instead of physical pin numbers
	GPIO.setmode(GPIO.BCM)

#	Define GPIO to use on Pi
	GPIO_PIR = 17

#	Path to LED script.
	ledOnpath = "/home/pi/rpi_framework/pi_led_state_change_on.py"
	ledOffpath = "/home/pi/rpi_framework/pi_led_state_change_off.py"



	print "PIR Module Test (CTRL-C to exit)"

#	Set pin as input
	GPIO.setup(GPIO_PIR,GPIO.IN)

	Current_State  = 0
#	Previous_State = 0

	try:

		print "Waiting for PIR to settle ..."

#	Loop until PIR output is 0
		while GPIO.input(GPIO_PIR)==1:
			Motion_State = 0

			print "  Ready."

#	Loop until user quits with CTRL-C
  		while True :

#	Read PIR state
			Motion_State = GPIO.input(GPIO_PIR)
#			read_ledstatusfile = open(ledstatusInPath, 'r')
#			Current_State_Regex = read_ledstatusfile.read()
#			Current_State = re.sub(r'2=', "", Current_State_Regex)
#			read_ledstatusfile.close()

	        	dbconn = sqlite3.connect(ledstatusPath)
        		dbcursor = dbconn.cursor()

        		led_status = True

                	dbconn.text_factory = str
                	dbcursor.execute('SELECT * FROM led_status')
               		Current_State = dbcursor.fetchall()
			response_compiled_regex = re.compile(regex_pattern)
	
			if Current_State=='0\n' and Motion_State==1:
				print(Current_State)
#	PIR is triggered
				print "  Motion detected, turning lights on!"
	
				os.system(ledOnpath)
				print "  Ready."

			elif Current_State=='0.6\n' and Motion_State==1:
#	PIR has returned to ready state
				print(Current_State)
				print "  Motion detected, turning lights off!"

      				os.system(ledOffpath)
				print "  Ready."
	
			elif Current_State<>'0.6\n' and Current_State<>'0\n':
#	PIR has returned to ready state
				print(Current_State)
				print "  Motion detected, turning lights off!"

				os.system(ledOffpath)
				print "  Ready."

#	Wait for 10 milliseconds
			time.sleep(.01)

	except KeyboardInterrupt:
       		signal_handler(signal.SIGINT, signal_handler)
#os.close(ledstatusInPath)

def piread():
#	 Communicate with another process through named pipe
#	 This is for reading only, as the pi-blaster is the writer.
	
	try:

#	Path to the pipe we should be reading from.  Notice that it is different than the actual
#		pi-blaster path.  Since we are dealing with fifo, then we cannot use the same pipe
#		as it is being read by the pi-blaster "C" process.  The led_status_change script
#		iterations will be writing to both the pi-blaster and the led_status_monitor.
#	piblasterPath = '/dev/pi-blaster'
		piblasterPath = '/tmp/led_status_monitor'

#	Path to the sqlite3 database.
	        ledstatusOutPath = '/tmp/monitoring_daemon.db'

#	Setup the sqlite3 data connections context.
	        dbconn = sqlite3.connect(ledstatusOutPath)
        	dbcursor = dbconn.cursor()


#	Setup the file descriptors for the status monitoring pipe.
		read_piblasterPath = os.open(piblasterPath, os.O_RDONLY)
#		read_piblasterPath = os.open(piblasterPath, os.O_RDONLY | os.O_CREAT)


		dbconn.text_factory = str # Use the text factory to remove the pesky sqlite brackets on read.

#	Execute a select all from the led_status table and read the state in, remove last state.
		response_orig = dbcursor.execute('SELECT * FROM led_status')
		response_orig = dbcursor.fetchall()
		for i in response_orig:
#			print i
			dbcursor.execute('DELETE FROM led_status WHERE state=?', i)
			dbconn.commit()

#	Initialize the response_orig value.
		response_orig = ''

#	print len(response_orig)

#	Configure the loop for reads.
		led_while_infinite = True # Set this to 1 for an infinite loop.


#	Start the while loop  May want to replace this with a select() statement to save cycles.
		while led_while_infinite == True : # Infinite Loop
		

#	Read in from the named pipe.
			response = os.read(read_piblasterPath, 4096)

#	Since this is for the LEDs and they are reading from the GPIO 2, then string that from the input
#		before insertion into the database.
			response_regexd = re.sub(r'2=', '', response)
		
			response_compiled_regex = re.compile(regex_pattern)

#	Loop to iterate and sort through the values to place them in the correct order.
			for i in response_compiled_regex.finditer(response_regexd):

				regex_finditer_output =  "%s" % (i.group(0))
				regex_finditer_output = `regex_finditer_output`
#				print regex_finditer_output

#	Database operations

				if response_orig == '':
					dbcursor.execute('INSERT INTO led_status (state) VALUES (?)', [regex_finditer_output])
					dbconn.commit()

				else:	
					dbcursor.execute('DELETE FROM led_status WHERE state=?', [response_orig])
					dbcursor.execute('INSERT INTO led_status (state) VALUES (?)', [regex_finditer_output])
					dbconn.commit()

				response_orig = regex_finditer_output
#				print 'Original response:  %s ' % (response_orig)
	except KeyboardInterrupt:
		signal_handler(signal.SIGINT, signal_handler)

def signal_handler(signal, frame):
#	Handling the ctrl+C to trigger removal of the FIFO and running other cleanup.
	picleanup()
	print 'Closing due to Signal Interupt: "Ctrl+C"'
	sys.exit(0)


def pimkfifo():
#	Create the FIFO named pipe in /dev.
				
	tmpdir = '/tmp' # Path for the tmp file.
	global tmpfilename
	tmpfilename = os.path.join(tmpdir, 'led_status_monitor') # Tmp file name.
#	print filename
	try:
		os.mkfifo(tmpfilename, 0664) # Create the pipe for monitoring and set permissions.
	except OSError, e:
		print "Failed to create FIFO: %s" % e # Print out any errors and exit.
#	else:
#		tmpfilename.close()	# Close the file path if an error occurs.
#		os.remove(tmpfilename) # File path to remove.


def pidbcheck():
	# Check for the existance of the database, if it is missing, create it.

	try:
		if not os.path.isfile(ledstatusOutPath):
			pidbcreate()
			pitablecreate()
			print 'Database verfication complete.'

		elif os.path.isfile(ledstatusOutPath):
			dbconn = sqlite3.connect(ledstatusOutPath)
			dbcursor = dbconn.cursor()
			print 'Database file exists, checking table status.'
			pitablecreate()
			print 'Database verfication complete.'
	
	
	except IOError:
		print 'Trouble executing database check.'


def pidbcreate():
	# If the DB does not exist, create it.

	try:
		print 'Database does not exist, creating.'
		dbconn = sqlite3.connect(ledstatusOutPath)
		dbcursor = dbconn.cursor()
		print 'Database created...'
	
	except IOError:
		print 'Could not create database.'


def pitablecreate():
	# Create the table if it does not exist.
	response_init  = ('initialize',)

	try:
		dbconn = sqlite3.connect(ledstatusOutPath)
		dbcursor = dbconn.cursor()
		
		dbcursor.execute('CREATE TABLE led_status (state)')
		dbcursor.execute('INSERT INTO led_status (state) VALUES (?)', response_init)

		dbconn.commit()
	
		print 'Tables created...'

	except sqlite3.OperationalError, e:
		print 'Trouble executing table creation, table already created.'


def picleanup():
#	Cleanup after script completion.
	
#	tmpfilename.close()	# Close the file path if an error occurs.
	os.remove(tmpfilename) # File path to remove.
	os.system('echo "2=0.0" > /dev/pi-blaster')

#	Reset GPIO settings
	GPIO.cleanup()


#class MyDaemon(daemon):
#	def run(self):
#		while True:
#			pimkfifo()
#			pidbcheck()
#			piread()
#			picleanup()
#		time.sleep(1)

if __name__ == '__main__':
	pimkfifo()
	pidbcheck()
	Thread(target = piread).start()
	time.sleep(5)
	Thread(target = pimotion).start()
#        daemon = MyDaemon('/tmp/daemon-stepper.pid')
#        if len(sys.argv) == 2:
#                if 'start' == sys.argv[1]:
#                        daemon.start()
#                elif 'stop' == sys.argv[1]:
#                        daemon.stop()
#                elif 'restart' == sys.argv[1]:
#                        daemon.restart()
#                else:
#                        print "Unknown command"
#                        sys.exit(2)
#                sys.exit(0)
#        else:
#                print "usage: %s start|stop|restart" % sys.argv[0]
#                sys.exit(2)
#pimkfifo()
#pidbcheck()
#piread()
#picleanup()
#########piwrite()

