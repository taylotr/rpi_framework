#!/usr/bin/env python
import os, time, sys
fifoname = '/dev/pi-blaster'                       # must open same name

def child( ):
    pipeout = os.open(fifoname, os.O_WRONLY)     # open fifo pipe file as fd
    zzz = 0
    while 1:
        time.sleep(zzz)
        os.write(pipeout, 'Spam %03d\n' % zzz)
        zzz = (zzz+1) % 5

def parent( ):
    pipein = open(fifoname, 'r', 0)                 # open fifo as stdio object
    while 1:
        line = pipein.readline( )[:-1]            # blocks until data sent
        print 'Parent %d got "%s" at %s' % (os.getpid(), line, time.time( ))

#if _ _name_ _ == '_ _main_ _':
#    if not os.path.exists(fifoname):
#        os.mkfifo(fifoname)                       # create a named pipe file
#    if len(sys.argv) == 1:
#        parent( )                                 # run as parent if no args
#    else:                                         # else run as child process
parent( )
