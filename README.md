Project Created by: Benjamin Kenawell
Projected Create @ HackPSU on Apr 8, 2017

My project is ideally the barebones of a phone.  Since I believed developing a usable UI would push me outside the time requirements, the final product is instead a message board.  For example, when you walk to your bosses desk and find he/she is not there, it would be nice to know where he/she is.  I do not work in an office yet, but I do have a more personal motivation for this project.  I am a Resident Assistant here at Penn State and believe this would make a great "Where am I?" board, so that my residents know where I am. The highlight feature of this board is the ability to text your message and have it display on the eInk screen, which will hold your message even if it loses power.  There are 5 buttons along the top of the screen, 3 are set aside for personalized messages, 1 is to update the weather, and the last button stores the last message texted (or given via a shell).  I have also included a Flask server implementation that allows a user to change the preset messages.  They cannot, as of yet, do more than that.
Additionally, the screen can be changed from a terminal.  The next step of the project is to create a web interface where the predefined button messages can be reset as well as the current message on the screen.  Due to wifi restrictions in many places of business, I was looking toward using an ESP8266 wifi chip as an access point.  Additionally, the RPi3 has bluetooth capability, so another step would be to interface with bluetooth.

My project uses the following hardware:
Raspberry Pi 3
PaPiRus Zero 2.0" eInk Screen
Adafruit FONA MiniGSM

My project uses the following programming languages and APIs:
Python
AT commands (https://cdn-shop.adafruit.com/product-files/1946/SIM800+Series_AT+Command+Manual_V1.09.pdf)
Wolfram Alpha API

My project uses the following Python libraries:
Serial
PaPiRus (https://github.com/PiSupply/PaPiRus)
threading
time
wolframalpha (https://pypi.python.org/pypi/wolframalpha/1.0)
RPi.GPIO
sys
Flask
File IO
