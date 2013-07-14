#!/usr/bin/env python


#      Author - TT
#      Creation Date - 05/09/13
#      Modification Date - 05/09/13
#      Script Name - pi_daemon_blaster.py
#      Description - The intent of this daemon is to monitor the /dev/pi-blaster named pipe.  It writes to a
#			sqlite3 database to retain persistence across reboots.
#      Aditional Authors Notes - 
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

import sys, time, os, sqlite3, re
from pi_daemon_external import daemon


ledstatusOutPath = '/tmp/led_stepper_status.db'
regex_pattern = r'[0-9.]+'


def piread():
	# Communicate with another process through named pipe
	# This is for reading only, as the pi-blaster is the writer.
	#piblasterPath = '/dev/pi-blaster'
	piblasterPath = '/dev/ttout'

        ledstatusOutPath = '/tmp/led_stepper_status.db'

        conn = sqlite3.connect(ledstatusOutPath)
        cursor = conn.cursor()


	read_piblasterPath = os.open(piblasterPath, os.O_RDONLY)
	led_while_infinite = True # Set this to 1 for an infinite loop.

	conn.text_factory = str
	response_orig = cursor.execute('SELECT * FROM led_status')
	response_orig = cursor.fetchall()
	for i in response_orig:
		print i
		cursor.execute('DELETE FROM led_status WHERE state=?', i)
		conn.commit()

	response_orig = ''

	print len(response_orig)

	while led_while_infinite == True : # Infinite Loop
		

		response = os.read(read_piblasterPath, 4096)

		response_regexd = re.sub(r'2=', '', response)
		
		response_compiled_regex = re.compile(regex_pattern)

		for i in response_compiled_regex.finditer(response_regexd):

			regex_finditer_output =  "%s" % (i.group(0))
			regex_finditer_output = `regex_finditer_output`
			print regex_finditer_output

			# Database operations

			if response_orig == '':
				cursor.execute('INSERT INTO led_status (state) VALUES (?)', [regex_finditer_output])
				conn.commit()

			else:	
				cursor.execute('DELETE FROM led_status WHERE state=?', [response_orig])
				cursor.execute('INSERT INTO led_status (state) VALUES (?)', [regex_finditer_output])
				conn.commit()

			response_orig = regex_finditer_output
#			print 'Original response:  %s ' % (response_orig)
		

def pidbcheck():
	# Check for the existance of the database, if it is missing, create it.

	try:
		if not os.path.isfile(ledstatusOutPath):
			pidbcreate()
			pitablecreate()
			print 'Database verfication complete.'

		elif os.path.isfile(ledstatusOutPath):
			conn = sqlite3.connect(ledstatusOutPath)
			cursor = conn.cursor()
			print 'Database file exists, checking table status.'
			pitablecreate()
			print 'Database verfication complete.'
	
	
	except IOError:
		print 'Trouble executing database check.'


def pidbcreate():
	# If the DB does not exist, create it.

	try:
		print 'Database does not exist, creating.'
		conn = sqlite3.connect(ledstatusOutPath)
		cursor = conn.cursor()
		print 'Database created...'
	
	except IOError:
		print 'Could not create database.'


def pitablecreate():
	# Create the table if it does not exist.
	response_init  = ('initialize',)

	try:
		conn = sqlite3.connect(ledstatusOutPath)
		cursor = conn.cursor()
		
		cursor.execute('CREATE TABLE led_status (state)')
		cursor.execute('INSERT INTO led_status (state) VALUES (?)', response_init)

		conn.commit()
	
		print 'Tables created...'

	except sqlite3.OperationalError, e:
		print 'Trouble executing table creation, table already created.'


pidbcheck()
piread()
#########piwrite()

#class MyDaemon(daemon):
#	def run(self):
#		while True:
#			picode()
#			time.sleep(1)

#if __name__ == "__main__":
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
#
