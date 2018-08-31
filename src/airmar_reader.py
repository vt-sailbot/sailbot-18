
#RX for ttyO1 - pin P9_26

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.UART as UART
import serial
import time
import binascii
import pynmea2
import math

import helmsman
import ship_data
import track_logger
import calc

airmar_heading_offset = 0

airmar_port = None

current_sentence = ""

print_airmar_input = False
print_airmar_sentence_contents = False

def setup():
     global airmar_port
     
#     try:
     airmar_port = serial.Serial(port="/dev/ttyO1", baudrate=4800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
#     except Exception as e:
#	     airmar_port = serial.Serial(port="/dev/ttyO0", baudrate=4800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

     airmar_port.open()

def clean(line):
	return ''.join(c for c in line if ord(c) >= 32)

def clean2(line):
	cleaned = ""
	for char in line:
		if(char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@$%^&*(),.<>[]{}1234567890 "):
			cleaned += char
	return cleaned

def read_airmar():	
    # TODO Read Airmar
        
    global current_sentence
    global airmar_port

    nToRead = 0
    try:
         nToRead = airmar_port.inWaiting()
    except:
#         airmar_port.close()
#         setup()
          nToRead = 0

#    print("reading " + str(nToRead))

    input = airmar_port.read(nToRead)

    for c in input:
	if(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$,./!@_+~`-=()[]<>{};'\|1234567890*"):
		current_sentence += c
	else:
		#process it
		if(print_airmar_input):
			print("got " + current_sentence)
			print(c)

		parse_line_and_update_ship_data(current_sentence)

		current_sentence = ""
    return

def parse_line_and_update_ship_data(line):
	if(len(line) < 2):
		return

	try:
		data = pynmea2.parse(line)
	except Exception, e:
		print(str(e))
#		track_logger.add_line(str(e), "errors")
		return

	try:
	
		contents = [field for tup in data.fields for field in tup]
	
	        if(print_airmar_sentence_contents):
	                print(contents)
	
			n = 1
			for var in contents:				
				if(str(var).lower() == var and ' ' not in str(var)):
					print(var + " -> " + str(getattr(data, var)))

				n += 1
	

	        if("Wind direction true" in contents and "wind_speed_meters" in contents and data.direction_true != None):
		    average_in_new_wind_data(float(data.direction_true), float(data.wind_speed_meters))
	#            ship_data.wind_heading = float(data.direction_true)
	#            ship_data.relative_wind_heading = (ship_data.wind_heading - ship_data.boat_heading) % 360
	#	    print(line)
		    wangle = float(data.direction_true)
	#            print("\t\t\tWIND ANGLE IN: " + str(wangle) + " WIND ANGLE: " + str(ship_data.wind_heading))
	            wind_speed = float(data.wind_speed_meters)
	#            print("\t\t\tWIND SPEED IN: " + str(wind_speed) + " WIND SPEED: " + str(ship_data.wind_speed))
	    
	        if("Latitude" in contents and data.latitude != None):
		    if(float(data.latitude) > 10):
		            ship_data.boat_lat = float(data.latitude)
	#	            print("\t\t\t\t\tLATITUDE: " + str(data.latitude))
		    
	
	        if("Longitude" in contents and data.longitude != None):
		    if(float(data.longitude) < -10):
			    ship_data.boat_lon = float(data.longitude)
			    ship_data.direction_to_target = calc.direction_to_point((ship_data.boat_lat, ship_data.boat_lon), ship_data.target_points[ship_data.targetI])
			    ship_data.current_distance_to_target = calc.distance((ship_data.boat_lat, ship_data.boat_lon), ship_data.target_points[ship_data.targetI])
	#	            print("\t\t\t\t\tLONGITUDE: " + str(data.longitude))

	#        if("altitude" in contents):
	#            ship_data.boat_altitude = float(data.altitude)
	    
	        if("heading" in contents and data.heading != None):
	            ship_data.boat_heading = (float(data.heading) + airmar_heading_offset)%360
	#            print("\t\t\t\t\tHEADING: " + str(data.heading))
	
	        if("speed" in contents and data.speed != None):
		            ship_data.boat_speed = float(data.speed)
	
	except Exception, e:
		print(e)
		track_logger.add_line(str(e) + " caused by", "errors")
		track_logger.add_line(line, "errors")
	

def average_in_new_wind_data(newWDir, newWS):

	#put new and old wind directions in radians
        newWDir *= 3.1415926535/180
        wDir = ship_data.wind_heading*3.14159265/180

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

        ship_data.wind_speed = s
        ship_data.wind_heading = heading
        ship_data.relative_wind_heading = (ship_data.wind_heading - ship_data.boat_heading)%360

