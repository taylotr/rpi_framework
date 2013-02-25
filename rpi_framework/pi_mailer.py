#! /usr/bin/python

#	Author - TT
#	Creation Date - 02/24/13
#	Modification Date - 02/24/13
#	Script Name - pi_mailer.py
#	Description - The intent of this script is to provide the framework for any messages sent
#		on the RPi sensor network. 
#	Aditional Authors Notes - This script is an amalgum of pieces I learned, the commandline 
#		arguments are taken from hamsoftengineering.com, special thanks to them.
#	Changelog:
#	    02/03/13 - Script started.
#	Usage Notes:
#		pythonEmail.py <from> <to> <subject> <bodyText> <smtpHost> <username> <password> <port>
#
# 		Input parameters:
#		sys.argv[1] is the sender email address
#		sys.argv[2] is the reciever email address,this can be a comma separated 
#			string for multiple recievers
#		sys.argv[3] is the subject text
#		sys.argv[4] is the body text
#		sys.argv[5] is the smtp host
#		sys.argv[6] is the smtp username
#		sys.argv[7] is the smtp password
#		sys.argv[8] is the smtp port


import sys, smtplib, email, time
 
# Are there enough arguments?  If not, print out the help.
if len(sys.argv) != 9:
	print 'Usage: pythonEmail.py <sender> <receiver> <subj> <bodyText> <smptHost> <username> <passwd> <port>'
	sys.exit(1)

# Variable Declaration
sender = sys.argv[1]		#  "From"
receiver = sys.argv[2]		#  "To"
subj = sys.argv[3]		#  "Subject"
bodyText = sys.argv[4]		#  "Body"
smtpHost = sys.argv[5]		#  Host - ie, gmail, yahoo, hotmail. etc...
username = sys.argv[6]		#  Username for host authentication
passwd = sys.argv[7]		#  Password for host authentication
port = sys.argv[8]		#  Port to use for host authentication
smtp_timeout = 'timeout=10';

def pi_print_debug():
	print (sender)
	print (receiver)
	print (subj)
	print (bodyText)
	print (smtpHost)
	print (username)
	print (passwd)
	print (port)
	print (smtp_timeout)


def pi_receiver_list():
# Create a list from the receiver in case we have a comma separated string of multiple receivers
	ReceiverList = []
	ReceiverList = receiver.split(',');



def pi_mailer_main():
# Actual mail to be sent
	server = smtplib.SMTP(smtpHost, port, smtp_timeout)
	server.starttls()
	server.ehlo()
	server.login(username, passwd)
	server.sendmail(sender, receiver, subj)
	server.quit()

pi_print_debug()

#try:
pi_receiver_list()
#except(RuntimeError), err:
#	print 'No list';


try:
	pi_mailer_main()
except(smtplib.SMTPSenderRefused), err:
	print "SMTP Sender Refused";
except(smtplib.SMTPAuthenticationError), err:
	print "SMTP Authentication Incorrect";


