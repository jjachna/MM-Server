from bottle import route, run
import serial
import RPi.GPIO as GPIO
import time
import thread

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.IN)

ser = serial.Serial('/dev/ttyAMA0', 1200)
ser.flush()
global running
global prevRunning

running = False
prevRunning = False

def checkGPIO():
	
	while True:
		#Check GPIO Pins for detection
		start = GPIO.input(24)
		end = GPIO.input(23)

		if (start == True):
			#print "Sensed it!!"
			global running
			running = True
		elif (end == True):
			#print "We done!!!!"
			global running
			running = False

		time.sleep(0.02)
	return None

@route('/connect')
def connect():
    return 'connected'

@route('/position/x=<x:float>_y=<y:float>')
def sendPosition(x, y):
	
	#Eliminate decimal and negative numbers
	x = (x + 90) * 10
	y = (y + 90) + 10
	
	#Position UART
	ser.write(str(x) + "-" + str(y) + "\0")
	
	read = ""
	#read = read + ser.read()
	#while not('\0' in read):
	#	read = read + ser.read()
		
	retVal = None
	if len(read) > 0:
		print read
		retVal = read
	elif running == True:
		if prevRunning == False:
			#print "Starting the Game!!!!"
			retVal = "GS"
		else:
			retVal = None
	elif running == False:
		if prevRunning == True:
			#print "Game completed!!!!"
			retVal = "T33.5"
		else:
			retval = None
	else:
		retVal = None
	global prevRunning
	prevRunning = running
	
	return retVal

@route('/getHighScore')
def getHighScores():
	ser.write("HS\0")

	read = ""
        #read = read + ser.read()
        #while not('\0' in read):
	#        read = read + ser.read()

        if len(read) > 0:
                return read
        else:
                return "33.7,44.3,45.6,49.4,60.0"

thread.start_new_thread(checkGPIO, ())
run(host='0.0.0.0', port=80, debug=False)

