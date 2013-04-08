#!/usr/bin/env python
import sys, time, os
from pi_daemon_external import daemon

def picode():
	# Communicate with another process through named pipe
	# This is for reading only, as the pi-blaster is the writer.
	piblasterPath = "/dev/pi-blaster"
	read_piblasterPath = os.open(piblasterPath, os.O_RDONLY)




	led_while = 1 # Set this to 1 for an infinite loop.
	while led_while == 1 : # Infinite Loop
		response = os.read(read_piblasterPath, 1024)


		ledstatusOutPath = "/tmp/led_stepper_status"
		write_ledstatusOut = open(ledstatusOutPath, 'w', 0)
		write_ledstatusOut.write(response)

	os.close(read_piblasterPath)

class MyDaemon(daemon):
	def run(self):
		while True:
			picode()
			time.sleep(1)

if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-stepper.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)

