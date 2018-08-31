import ship_data, captain

import time

import math

file_name = "tracks/log_" + str(math.floor(time.time()))
file = open(file_name, 'w')

captain = None

def setup(c):
	global captain
	captain = c

def log():
	file.write(str((ship_data.boat_lat, ship_data.boat_lon, ship_data.boat_heading, captain.current_desired_heading, ship_data.wind_heading, ship_data.wind_speed, ship_data.targetI, ship_data.auto, time.time())))
	file.write("\n")

def add_line(s, filename):
                file = open(filename, 'r')
                errors = ""
                for line in file:
                        errors += line
                errors += s
                errors += '\n'
		file.close()

                file2 = open(filename, 'r+')
                file2.write(errors)
		file2.close()
