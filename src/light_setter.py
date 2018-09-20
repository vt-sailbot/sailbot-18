import Adafruit_BBIO.GPIO as GPIO

light_pin = "P8_12"

def setup():
	"""
	Sets up the specified light pin
	"""
	GPIO.setup(light_pin, GPIO.OUT)

def set_light(on):
	"""
	Turns the light on or off

	Keyword arguments:
	on -- Truthy value to turn on light, falsy value to turn off light
	"""
	if(on):
		GPIO.output(light_pin, GPIO.HIGH)
	else:
		GPIO.output(light_pin, GPIO.LOW)
