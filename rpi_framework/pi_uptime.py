#! /usr/bin/python

from datetime import timedelta

# Variable Declaration

def ttuptime():
# Determine the uptime
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds))

		print(uptime_string)

#try:
ttuptime()


