#! /usr/bin/python

# Import necessary modules
#import socket, subprocess, re

# Variable Declaration
#Loopback = "Local Loopback:"

#def pistepper():
def pistepper(start, stop, step):
    r = start
    while r < stop:
	yield r
	print(r)
	r += step



# Call Subroutine
i0=pistepper(0.0, 1.0, 0.025)
