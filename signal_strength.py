#!/usr/bin/python

from serial import Serial

fona = Serial('/dev/ttyUSB0')
fona.write(b'AT+CSQ\n')
line = fona.readline().strip()
print(line)
while(not(line == "OK")):
	line = fona.readline().strip()
	print(line)
#line = fona.readline().strip()
#fona.readline().strip()
#fona.readline().strip()

#line = line.split(',')
#print(line[1])
