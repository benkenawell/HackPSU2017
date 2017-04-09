#!/usr/bin/python

from serial import Serial

fona = Serial('/dev/ttyUSB1')
fona.write(b'AT+CMGL=\"REC UNREAD\"\n')
line = fona.readline().strip()
print(line)
while(not(line == "OK")):
	line = fona.readline().strip()
	print(line)
