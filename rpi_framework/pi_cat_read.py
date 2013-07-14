#!/usr/bin/env python
import sys, time, os, sqlite3, subprocess

def picode():
        ledstatusOutPath = '/tmp/monitoring_daemon.db'

        conn = sqlite3.connect(ledstatusOutPath)
        cursor = conn.cursor()
	
#	led_stat = subprocess.call(["cat", "<", "/dev/pi-blaster"])

       	led_status = True

        try:
#               while led_status == True:
#		cursor.execute('SELECT * FROM led_status order by rowid limit 1')
		conn.text_factory = str
             	cursor.execute('SELECT * FROM led_status')
               	led_status_out = cursor.fetchall()

		for i in led_status_out:
			print i


        finally:

                print 'Closed.'




picode()

