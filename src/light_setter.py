import Adafruit_BBIO.GPIO as GPIO

light_pin = "P8_12"

def setup():
	GPIO.setup(light_pin, GPIO.OUT)

def set_light(on):
	if(on):
		GPIO.output(light_pin, GPIO.HIGH)
	else:
		GPIO.output(light_pin, GPIO.LOW)

