#RX for ttyO1 - pin P9_26

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.UART as UART
import serial
import time
import binascii
import pynmea2
import math
#import numpy as np
import os

from helmsman import Helmsman
import ship_data
import track_logger
import arduino_signaler
import airmar_reader
from calc import Point

#rudder, sail, auto_switch, other_switch
RC_inputs = [0, 0, 0, 0]

airmar_heading_offset = 0

#zero points for RC angles from the Arduino
rudder_baseline = -20;

#zero points for angles sent to the Arduino
left_rudder_zero_point = 0;
right_rudder_zero_point = 0;

auto_switch_times = []
other_switch_times = []

helmsman = None

def setup(h):
	"""
	Runs setup methods for airmar and arduino from airmar_reader and arduino_signaler

        KWargs:
        h -- helmsman module 
	
        Returns:
        n/a
    
        Side effects:
        Runs setup methods on airmar_reader and arduino_signaler
        """ 
	global helmsman
	helmsman = h
	#os.system("echo BB-UART1 > /sys/devices/bone_capemgr.*/slots")
	os.system("./open_airmar_port")		#deprecated... use subprocess module instead
	airmar_reader.setup()

##ARDUINO COMMUNICATION CURRENTLY ON
	arduino_signaler.setup()

def average_in_new_wind_data(newWDir, newWS):
	"""
	Sets wind_speed, wind_heading, and relative_wind_heading in the ship_data module

        KWargs:
        newWDir -- new wind direction
        newWS -- new wind speed

        Returns:
        n/a

        Side effects:
        Changes wind_speed, wind_heading, and relative_wind_heading values in ship_data module
	
        **** DUPLICATE OF FUNCTION IN airmar_reader.py ****

	"""

	
	newWDir *= 3.1415926535/180			#np.pi/180

	wDir = ship_data.wind_heading*3.14159265/180	#wDir = shipdata.wind_heading*(np.pi/180)
	wS = ship_data.wind_speed

	oldX = wS*math.sin(wDir)
	oldY = wS*math.cos(wDir)

	newX = newWS*math.sin(newWDir)
	newY = newWS*math.cos(newWDir)

	newWeight = .3
	x = oldX*(1 - newWeight) + newX*newWeight
	y = oldY*(1 - newWeight) + newY*newWeight

	s = math.sqrt(x*x + y*y)
	heading = (math.atan2(x, y)*180/math.pi)%360

	ship_data.wind_speed = s		#why are you defining s separately?
	ship_data.wind_heading = heading
	ship_data.relative_wind_heading = (ship_data.wind_heading - ship_data.boat_heading)%360


def signal_arduino():
	"""
	Reads rudder and winch angle from RC_inputs and determines if auto or other... Writes target and zero point for left and right rudder angle, winch angle
	"""
	global auto_switch_times
	global other_switch_times
	global left_rudder_zero_point
	global right_rudder_zero_point

	RC_inputs = arduino_signaler.read_arduino()
	if(RC_inputs == []):
		print("NO DATA FROM ARDUINO")
		return

	if(arduino_signaler.print_received_signals):
		print("RC input: " + str(RC_inputs))

	ship_data.RC_rudder_angle = RC_inputs[0]
	ship_data.RC_winch_angle = RC_inputs[1]

	old_auto = ship_data.auto
	old_other = ship_data.other
	ship_data.auto = (RC_inputs[2] == 1)
	ship_data.other = (RC_inputs[3] == 1)

	if(old_auto != ship_data.auto):
		auto_switch_times.append(time.time())
	if(old_other != ship_data.other):
		other_switch_times.append(time.time())

	#check for flips in last 10 seconds
	curT = time.time()
	auto_switch_times = [t for t in auto_switch_times if (curT - t) < 10]
	other_switch_times = [t for t in other_switch_times if (curT - t) < 10]

	#if the auto switch flips 5 times in 10 seconds and the boat's manual
	if(len(auto_switch_times) > 5 and not ship_data.auto):
		#make the left rudder's zero point the current position; zero the left rudder
		left_rudder_zero_point = ship_data.RC_rudder_angle + left_rudder_zero_point
		print("\nCALIBRATING LEFT RUDDER: " + str(left_rudder_zero_point))
		auto_switch_times = []

	#if the other switch flips 5 times in 10 seconds and the boat's manual
	if(len(other_switch_times) > 5 and not ship_data.auto):
		#make the right rudder's zero point the current position; zero the right rudder
		right_rudder_zero_point = ship_data.RC_rudder_angle + right_rudder_zero_point
		print("\nCALIBRATING RIGHT RUDDER: " + str(right_rudder_zero_point))
		other_switch_times = []

#	print(left_rudder_zero_point, right_rudder_zero_point)

	arduino_signaler.write_arduino(helmsman.target_rudder_angle + left_rudder_zero_point, helmsman.target_rudder_angle + right_rudder_zero_point, helmsman.target_winch_angle)


def check_airmar():
	"""
	Runs read_airmar method from airmar_reader module
	"""
	airmar_reader.read_airmar()
