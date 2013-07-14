#!/usr/bin/env python
import sys, time, os, sqlite3
from pi_daemon_external import daemon


ledstatusOutPath = "/tmp/led_stepper_status.db"


def picode():
	# Communicate with another process through named pipe
	# This is for reading only, as the pi-blaster is the writer.
	piblasterPath = "/dev/pi-blaster"
	ledstatusOutPath = "/tmp/led_stepper_status.db"

	read_piblasterPath = os.open(piblasterPath, os.O_RDONLY)

	conn = sqlite3.connect(ledstatusOutPath)
	cursor = conn.cursor()

	led_while_infinite = True # Set this to 1 for an infinite loop.

	response_orig  = os.read(read_piblasterPath, 16)

	while led_while_infinite == True : # Infinite Loop
		response = os.read(read_piblasterPath, 16)

		# Database operations
		cursor.execute(""" UPDATE led_status SET state=? """, (response,))

		#cursor.execute(""" UPDATE led_status SET state=? """, (response,))
		
		response_orig = response
		conn.commit()

#		# Database operations
#		sql = """
#			INSERT INTO led_status
#				(state)
#			VALUES
#				(?)
#			"""
#		#cursor.execute(""" UPDATE led_status SET state=? """, (response,))
#		data = [response]
#
#		cursor.execute(sql, data)
#		conn.commit()

		print response


	os.close(read_piblasterPath)



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

	try:
		conn = sqlite3.connect(ledstatusOutPath)
		cursor = conn.cursor()
		
		cursor.execute("""CREATE TABLE led_status (state)""")
#		cursor.execute("""CREATE TABLE led_status (led_status_id, state, state_orig)""")
		conn.commit()
	
		print 'Tables created...'

	except sqlite3.OperationalError, e:
		print 'Trouble executing table creation, table already created.'


pidbcheck()
picode()

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
