#!/usr/bin/env python
import sys, time, os, sqlite3, re

def picode():
	ledstatusOutPath = '/tmp/led_stepper_status.db'

	conn = sqlite3.connect(ledstatusOutPath)
	cursor = conn.cursor()

#	led_status = True

	try:
#		while led_status == True:
#		cursor.execute(""" SELECT * FROM led_status order by rowid limit 1""")
		conn.text_factory = str
		cursor.execute('SELECT * FROM led_status')
		led_status_out = cursor.fetchall()
		for i in led_status_out:
			print i

	finally:
		
		print 'Closed.'




picode()

