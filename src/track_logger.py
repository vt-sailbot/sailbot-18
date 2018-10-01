import ship_data, captain

import time

import math

file_name = "tracks/log_" + str(math.floor(time.time()))
file = open(file_name, 'w')

captain = None

def setup(c):
	"""
	Instantiates a captain object.		

	Keyword Arguments:
	c -- captain object

	Side effects:
	-Changes the global variable captain

	"""
	global captain
	captain = c

def log():
	"""
	Overwrites the current content of file with ship data.
	"""
	file.write(str((ship_data.boat_lat, ship_data.boat_lon, ship_data.boat_heading, captain.current_desired_heading, ship_data.wind_heading, ship_data.wind_speed, ship_data.targetI, ship_data.auto, time.time())))
	file.write("\n")

def add_line(s, filename):
	"""
	Adds line to file by creating a new file with all the text from the old file plus the new line.

	Keywords Arguments:
	s -- string added to end of file
	filename -- file name string
	"""
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
