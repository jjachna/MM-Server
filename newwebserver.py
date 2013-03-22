from bottle import route, run
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

GPIO.output(23, False)
GPIO.output(24, False)
GPIO.output(15, False)
GPIO.output(14, False)


@route('/connect')
def connect():
    return 'connected'

@route('/position/x=<x:float>_y=<y:float>')
def ledOn(x, y):
	if x >= 0:
		GPIO.output(14, True)
		GPIO.output(15, False)
	else:
		GPIO.output(15, True)
		GPIO.output(14, False)
	
	if y >= 0:
		GPIO.output(23, True)
		GPIO.output(24, False)
	else:
		GPIO.output(24, True)
		GPIO.output(23, False)
	
	return None

run(host='0.0.0.0', port=80, debug=False)