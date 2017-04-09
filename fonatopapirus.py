#!/usr/bin/python

from papirus import PapirusTextPos
from serial import Serial
import sys
import RPi.GPIO as GPIO
import threading
import time
import wolframalpha

SW1 = 21
SW2 = 16
SW3 = 20
SW4 = 19
SW5 = 26
SW = [21,16,20,19,26]
msg = ["SW1","SW2","SW3","SW4","SW5"]

def buttonPressed(channel):
	global lasttxt
	updateText = ""
	if(channel == SW[0]):
		updateText = "Here.  Just knock :)"
	elif(channel == SW[1]):
		updateText = "Away. Be back soon."
	elif(channel == SW[2]):
		updateText = "SW3"
	elif(channel == SW[3]):
		updateText = ""
		papi.UpdateText("weather", "--")
		papi.papirus.display(papi.image)
		papi.papirus.partial_update()
		weather_thread.getWeather()
	elif(channel == SW[4]):
		updateText =	lasttxt
	if(updateText != ""):
		papi.UpdateText("result",updateText)
		papi.papirus.display(papi.image)
		papi.papirus.partial_update()

class refreshScreen(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while(True):
			papi.WriteAll()
			time.sleep(60)

class updateTime(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.last_time = time.strftime("%H:%M")
		papi.UpdateText("time", self.last_time)
		papi.papirus.display(papi.image)
		papi.papirus.partial_update()
	def run(self):
		while(True):
			self.curr_time = time.strftime("%H:%M")
			if(self.curr_time != self.last_time):
				papi.UpdateText("time", self.curr_time)
				papi.papirus.display(papi.image)
				papi.papirus.partial_update()
			time.sleep(10)

class batlife(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while(True):
			fonaLock.acquire()
			fona.write(b'AT+CBC\n')
			fona.readline() #echoed cmd
			self.bat_line = fona.readline().strip()
			fona.readline()
			fona.readline()
			fonaLock.release()
			self.bat_line = self.bat_line.split(',')
			papi.UpdateText("bat", self.bat_line[1] + '%')
			papi.papirus.display(papi.image)
			papi.papirus.partial_update()
			time.sleep(60) #update battery life every minute

class weather(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.appid = "74PH97-WLV3Y3G8XR"
		self.client = wolframalpha.Client(self.appid)
	def run(self):
		while(True):
			self.getWeather()
			time.sleep(7200) # udpate every 2 hours
	def getWeather(self):
			self.res = self.client.query('temperature in State College, PA now')
			papi.UpdateText("weather", next(self.res.results).text[:5])
			papi.papirus.display(papi.image)
			papi.papirus.partial_update()

class phone(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global lasttxt
		while(True):
			fonaLock.acquire()
			line = fona.readline()
			fonaLock.release()
			#waiting for imput of some kind.
			# most of the polling will be done here
			while(not(line[:5] == "+CMTI")):
		#		for switch in range(len(SW)):
		#			if(GPIO.input(SW[switch]) == False):
		#				papi.write(msg[switch])
				fonaLock.acquire()
				line = fona.readline()
				fonaLock.release()
				time.sleep(2)
			fonaLock.acquire()
			fona.write(b'AT+CMGL=\"REC UNREAD\"\n')
			#fona.readline() #read echoed cmd
			while(not(line[:5] == "+CMGL")):
				#print(fona.readline()) #read the header information
				print(line)
				line = fona.readline()
			result = fona.readline().strip() # read the text message
			print(result)
			fona.readline() #empty line
			print(fona.readline().strip()) #status returned.  should be OK
			#papi.AddText(result, Id="result")
			fonaLock.release()
			lasttxt = result
			papi.UpdateText("result", result);
			#papi.WriteAll()
			#papi.write(result)
			papi.papirus.display(papi.image)
			papi.papirus.partial_update()

fonaLock = threading.Lock()
#start serial connection to fona
fona = Serial('/dev/ttyUSB1', timeout=1)
lasttxt = ""
#papi = PapirusTextPos(False)
#connect to papirus screen
papi = PapirusTextPos(False)
papi.AddText("", 0, 25, Id="result")
papi.AddText("", 0, 75, Id="bat")
papi.AddText("", 125, 75, Id="weather")
papi.AddText("", 50, 75, Id="time")
#menu options
papi.AddText("Last", 20, 0, Id="SW5", size=12)
papi.AddText("Wthr", 60, 0, Id="SW4", size=12)
papi.AddText("SW3", 90, 0, Id="SW3", size=12)
papi.AddText("Away", 120, 0, Id="SW2", size=12)
papi.AddText("Here", 160, 0, Id="SW1", size=12)
#setup switches on pins
GPIO.setmode(GPIO.BCM)

for switch in SW:
	GPIO.setup(switch, GPIO.IN)
	GPIO.add_event_detect(switch, GPIO.FALLING, callback=buttonPressed)

#start the other threads
bat_thread = batlife()
weather_thread = weather()
phone_thread = phone()
refresh_thread = refreshScreen()
time_thread = updateTime()
bat_thread.start()
weather_thread.start()
phone_thread.start()
refresh_thread.start()
time_thread.start()

fonaLock.acquire()
#setup the fona.  Make sure it is working
fona.write(b'AT\n')
fona.readline() #read the cmd I just sent
result = fona.readline().strip() #read the result and strip the nonprinting characters
fonaLock.release()
print(result)
if(not result == "OK"): sys.exit()
while(True):
	msg = raw_input('Enter message:')	
	lasttxt = msg
	papi.UpdateText("result", msg)
	papi.papirus.display(papi.image)
	papi.papirus.partial_update()
