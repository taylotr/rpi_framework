#!/usr/bin/python

import shelve

s = shelve.open('/home/pi/rpi_framework/pi_shelve_test.db')

try:
	s['key1'] = { 'int': 10, 'float':9.5, 'string':'sample data'}

finally:
	s.close()
