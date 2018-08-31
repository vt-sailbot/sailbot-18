import Adafruit_BBIO.PWM as pulser
import time


class ServoController:

    def __init__(self, pin, name, angle_limits):
	self.zero_point = 6.5

	self.writes = 0

        self.servo_pin = pin
        self.name = name
	self.min_angle = angle_limits[0]
	self.max_angle = angle_limits[1]

	print("starting servo signal at " + str(pin))
        pulser.start(self.servo_pin, 6.8, 60)

    def set_servo_angle(self, angle):
        # TODO Fix output

	if(angle < self.min_angle):
		angle = self.min_angle
	if(angle > self.max_angle):
		angle = self.max_angle

        w = (angle/30.0) + self.zero_point
        pulser.set_duty_cycle(self.servo_pin, w)

	if(self.writes % 10 == 0):
	        print(str(self.name) + ": " + str(angle) + "   " + str(w));
	self.writes += 1
