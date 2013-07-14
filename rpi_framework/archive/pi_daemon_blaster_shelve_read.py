#!/usr/bin/env python
import sys, time, os, shelve

def picode():
	ledstatusOutPath = "/tmp/led_stepper_status.db"

	led_shelve_out = shelve.open(ledstatusOutPath)

	try:
		led_shelve_read = led_shelve_out['led_key1']

	finally:
		led_shelve_out.close()

	print led_shelve_read




picode()

