#!/usr/bin/env python
import io

with open('/dev/pi-blaster', 'r', 0) as tt:
	i = tt.readall('/dev/pi-blaster')
	print i
