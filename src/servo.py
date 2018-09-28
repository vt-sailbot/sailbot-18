import Adafruit_BBIO.PWM as pulser
import time


class ServoController:
    """
    Sets up and manages a servo
    """

    def __init__(self, pin, name, angle_limits):
        """
        Instantiates a new servo with implementation details

        Keyword arguments:
        self -- The caller, the new instance
        pin -- The signal pin for the servo
        name -- The name of the servo, for debugging purposes (should be optional)
        angle_limits -- A length 2 array in the format [min angle, max angle]

        Side effects:
        - Sets instance variables
        """
        self.zero_point = 6.5 # Very implementation-specific, should be defined elsewhere
        self.writes = 0 # Why are we storing this?

        self.servo_pin = pin
        self.name = name

        self.min_angle = angle_limits[0]
        self.max_angle = angle_limits[1]

        print("starting servo signal at " + str(pin))
        pulser.start(self.servo_pin, 6.8, 60)

    def set_servo_angle(self, angle):
        """
        Sets the servo angle

        Keyword arguments:
        self -- The caller, the instance
        angle -- The angle at which to set the servo
        """
        # TODO Fix output

        if(angle < self.min_angle):
            angle = self.min_angle
        if(angle > self.max_angle):
            angle = self.max_angle

        w = (angle/30.0) + self.zero_point
        pulser.set_duty_cycle(self.servo_pin, w)

        if(self.writes % 10 == 0):
            print(str(self.name) + ": " + str(angle) + "   " + str(w))
        self.writes += 1
