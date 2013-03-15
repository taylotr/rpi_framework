#!/bin/bash

x=1
while [ $x -le 5 ]
do 

	for i in `cat pi_ledstrip.in`; do echo "$i" > /dev/pi-blaster; sleep 0.1; done
	x=$(( $x +1))
done
