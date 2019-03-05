#!/usr/bin/env python
import time
from grovepi import pinMode,digitalRead
from grove_rgb_lcd import setText,setRGB

# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND
button = 3

pinMode(button,"INPUT")

setText("READY")
setRGB(0,0,255)

while True:
	try:
		state = digitalRead(button)

	except IOError:
		print ("Button Error")

	time.sleep(.1)
	if state == 1:
		print ("button pushed")
		break

setText("Done!")
setRGB(0,255,0) 
