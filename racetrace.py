#!/usr/bin/env python
import time
import signal
import sys
from grovepi import pinMode,digitalRead,analogRead,digitalWrite
from grove_rgb_lcd import setText,setRGB

# Connect the Grove Light Sensor to analog port A0
light_sensor = 0

# Connect the Grove Button to digital port D3
button = 3

# Connect the Relay to digital port D5
relay = 5

# Connect the LED to digital port D6
led = 6

# light sensor sample threshold difference
threshold = 80

pinMode(light_sensor,"INPUT")
pinMode(button,"INPUT")
pinMode(led,"OUTPUT")
pinMode(relay,"OUTPUT")

def signal_handler(sig, frame):
	digitalWrite(relay,0)
	digitalWrite(led,0)
	setRGB(0,0,0)
	setText("")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def turnOnLED():
	digitalWrite(led,1)

def turnOffLED():
	digitalWrite(led,0)

def turnOnRelay():
	digitalWrite(relay,1)

def turnOffRelay():
	digitalWrite(relay,0)

def startingGateReady():
	turnOnRelay()
	setText("READY")
	setRGB(0,0,255)

def readLightSensor():
	return analogRead(light_sensor)

def waitForButtonPress():
	while True:
		try:
			state = digitalRead(button)

		except IOError:
			print ("Button Error")

		time.sleep(.1)
		if state == 1:
			print ("button pushed")
			break

def runRace():
	setText("Running!!!")
	setRGB(0,255,0) 
	bg = readLightSensor()
	turnOnLED()
	turnOffRelay()
	start_time = time.time()

	while True:
		try:
			sensor_value = readLightSensor()

		except IOError:
			print ("Light Sensor Error")

		if (sensor_value + threshold) < bg:
			break

		time.sleep(.01)

	turnOffLED()
	return (time.time() - start_time)

def displayResults(elaped_time):
	mph = 9.2045 / elapsed_time
	timestr = "elapsed: %.3fs\nMPH: %.3f" % (elapsed_time, mph)
	print (timestr)
	setText(timestr)
	setRGB(255,0,0)

while True:
	startingGateReady()
	waitForButtonPress()
	elapsed_time = runRace()
	displayResults(elapsed_time)
	waitForButtonPress()
