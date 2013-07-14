#!/usr/bin/python

import shelve

s = shelve.open('/home/pi/rpi_framework/pi_shelve_test.db')

try:

	existing = s['key1']

finally:
	s.close()

print existing
