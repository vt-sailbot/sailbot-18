#!/usr/bin/env python
import os
import traceback
from captain import Captain
from helmsman import Helmsman
from stoppable_thread import StoppableThread
import ship_data
import data_sender
import calc
from calc import Point
import sensor_communicator
import utils
import track_logger

import light_setter

import cOM_test

import threading
import time
from random import random

"""
Sets up and manages the Airmar sensor, starts and updates the captain and helmsman, manages waypoint detection.
"""

#delays in seconds
sensor_thread_delay = .01
main_loop_delay = .1

timestep = 0

captain = None
helmsman = None
sensor_thread = None

start_time = time.time()

debug_mode = False

"""
Prints out debug info.

There has to be a cleaner way to do this.
"""
def debug():
	timeRunning = time.time() - start_time
	# ship_data.wind_heading = 40
	#
	# light_setter.set_light(timeRunning % 2 < 1)

	#print things for debugging
	if (timestep % 10 == 0):
		print("\t\t\t\t\tcurrent position: " + str((ship_data.boat_lat, ship_data.boat_lon)))

		print("current distance to target: " + str(current_proximity))

	        print("\ncDH: " + str(captain.current_desired_heading) + '; now facing ' + str(ship_data.boat_heading))
	        print("wind: " + str(ship_data.wind_heading))

	        relative_wind_angle = ship_data.relative_wind_heading
	        if(relative_wind_angle > 180):
      		        relative_wind_angle = 360 - relative_wind_angle

		print("relative wind: " + str(relative_wind_angle))
	        print(ship_data.boat_lat, ship_data.boat_lon)
	        print(ship_data.direction_to_target)
	        print(ship_data.rudder_servo_angle)
		print("auto: " + str(ship_data.auto))

		ship_data_names = [item for item in dir(ship_data) if not item.startswith("__")]

		for name in ship_data_names:
			print(name + ": " + str(getattr(ship_data, name)))

		print("captain.current_desired_heading: " + str(captain.current_desired_heading))

		print("captain.current_fastest_midpoint: " + str(captain.current_fastest_midpoint))

		print("captain.current_target: " + str(captain.current_target))

		print("helmsman.target_rudder_angle: " + str(helmsman.target_rudder_angle))

		print("\n\n")


"""
Reads and updates the Airmar and RC controller.

Why is this a class? This should also be somewhere else.
"""
class SensorThread(StoppableThread):

	"""
	Sets up and continually updates the Airmar and Arduino.
	"""
    def run(self):
		sensor_communicator.setup(helmsman)

        sensorThreadRunI = 0

        while (True):
	    	sensorThreadRunI += 1
			time.sleep(sensor_thread_delay)
	    	try:
	            if self.stopped():
					print("SensorThread stopped")
					track_logger.add_line("STOPPED", "errors")
	                break

			# ARDUINO COMMUNICATION TURNED ON
		    sensor_communicator.signal_arduino()

		    sensor_communicator.check_airmar()
		    ship_data.wind_heading = sensorThreadRunI / 3

		    if (sensorThreadRunI % 10 == 0):
			    data_sender.send_update()

		    except Exception, e:
				eStr = "in Sensor Thread: " + str(e)
				track_logger.add_line(eStr, "errors")
		        print(eStr)
				traceback.print_exc()
				break

"""
Runs if waypoint is hit
"""
def check_waypoint_proximity():
    if(within_radius_of_target()):
        ship_data.targetI += 1
		ship_data.targetI %= len(ship_data.target_points)
        print("******************************** HIT WAYPOINT " + str(ship_data.targetI) +  " ************************************")

"""
Checks to see if waypoint is hit.

This and check_waypoint_proximity should be merged, and should be with other navigation code.
"""
def within_radius_of_target():
    current_point = [ship_data.boat_lat, ship_data.boat_lon]
    target_point = ship_data.target_points[ship_data.targetI]
    current_proximity = (calc.distance(current_point, target_point))
    return calc.within_radius_of_target(current_point, target_point)

"""
Starts all the captain, helmsman, and sensor services.
"""
def start_SailBot():
	global captain, helmsman, sensor_thread

	# Create captain instance
	print("setting up captain")
	captain = Captain()
	captain.setup()

	# Create helmsman listening to captain
	print("setting up helmsman")
	helmsman = Helmsman(captain)
	helmsman.setup()

	# Start Airmar and RC readin' loop
	print("setting up sensor communicator")
	sensor_thread = SensorThread()
	sensor_thread.start()

	print("starting finished")

	if (debug_mode):
		track_logger.setup(captain)
		light_setter.setup()

	ship_data.start_time = time.time()


# --------------------------------------------------- main loop --------------------------------------------------- #

# MAKE THE BOAT AUTONOMOUS
#ship_data.auto = True

print("STARTING SAILBOT")
start_SailBot()

"""
Updates captain and helmsman services until interrupt is caught.
"""
try:
	while(True):
		try:
	        if (debug_mode):
				debug()

			#check if the current waypoint is hit
			check_waypoint_proximity()

			if(ship_data.auto):
				captain.think()

	        	helmsman.steer_boat()

			if (debug_mode):
				track_logger.log()

			time.sleep(main_loop_delay)
			timestep += 1

		except Exception, e:
			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print(e)
			traceback.print_exc()

except (KeyboardInterrupt), e:
    print(str(e))
    print("^C CAUGHT - MAIN LOOP ENDING")
    sensor_thread.stop()
