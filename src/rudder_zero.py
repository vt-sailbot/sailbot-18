#!/usr/bin/env python
from captain import Captain
from helmsman import Helmsman
from stoppable_thread import StoppableThread
import ship_data
import calc
from calc import Point
import sensor_communicator
import utils

import threading
import time

#delays in seconds
sensor_thread_delay = .1
main_loop_delay = .1

timestep = 0

captain = None
helmsman = None
sensor_thread = None

# Reads the Airmar and RC controller
class SensorThread(StoppableThread):
    def run(self):
	sensor_communicator.setup()
        while(True):
	    try:
	            if self.stopped():
	                break
	            sensor_communicator.read_airmar()
		    sensor_communicator.read_rc_receiver()
	            time.sleep(sensor_thread_delay)
	    except Exception:
	        q = 1	
	
def check_waypoint_proximity():
    if(within_radius_of_target()):
        ship_data.targetI += 1
        print("******************************** HIT WAYPOINT " + str(ship_data.targetI) +  " ************************************")

def within_radius_of_target():
    current_point = Point([ship_data.boat_lat, ship_data.boat_lon])
    target_point = Point(ship_data.target_points[ship_data.targetI])
#    print(current_point.lat, current_point.lon)

    return calc.within_radius_of_target(current_point, target_point)


def start_SailBot():
	global captain, helmsman, sensor_thread

	# Create captain instance
	captain = Captain()
	captain.setup()
	# Create helmsman listening to captain
	helmsman = Helmsman(captain)
	helmsman.setup()
	
	# Start Airmar and RC readin' loop
	sensor_thread = SensorThread()
	sensor_thread.start()

#utils.setup_terminal_logging()

#utils.shutdown_terminal()

start_SailBot()

try:
	while(True):
		try:
			check_waypoint_proximity()
	
	        	time.sleep(main_loop_delay)
	        	captain.think()
			captain.current_desired_heading = ship_data.wind_heading		

			ship_data.auto = False	
			ship_data.RC_rudder_angle = 0
	        	helmsman.steer_boat()
	
#			if(timestep % 10 == 0):
#			        print("\ncDH: " + str(captain.current_desired_heading) + '; now facing ' + str(ship_data.boat_heading))
#			        print("wind: " + str(ship_data.wind_heading))
#				print("relative wind: " + str(ship_data.relative_wind_heading))
#			        print(ship_data.boat_lat, ship_data.boat_lon)
#			        #print(ship_data.direction_to_target)
#			        #print(ship_data.rudder_servo_angle)
#				print("auto: " + str(ship_data.auto))
			
			timestep += 1
		except KeyboardInterrupt, e:
			print(e)
			sensor_thread.stop()
			quit()
		except Exception:
			q = 1

except (KeyboardInterrupt, Exception), e:
    #print("main loop excepted")
    print(str(e))
    sensor_thread.stop()
#    utils.shutdown_terminal()

