#!/usr/bin/python

from serial import Serial

fona = Serial('/dev/ttyUSB1')
fona.write(b'AT+CMGF=1\n')
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
