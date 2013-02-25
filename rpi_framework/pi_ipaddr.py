#! /usr/bin/python

# Import necessary modules
import socket, subprocess, re

# Variable Declaration
Loopback = "Local Loopback:"

def ttipaddr():
# Get the IP address of the local machine
    p = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    ifc_resp = p.communicate()
    patt = re.compile(r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    resp = patt.findall(ifc_resp[0])


    print '\n' .join(resp)


# Call Subroutine
ttipaddr()


