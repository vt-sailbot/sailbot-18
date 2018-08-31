from math import *
from random import random
import calc
#from geopy.distance import vincenty

# a_s = 0
# x_s = 0
# y_s = 0
#
# x_e = 100
# y_e = 30
# a_e = 0
#
# wind_heading = 20

def angleFromNorth(lat1, lon1, lat2, lon2):
    lon1 = lon1*pi/180
    lat1 = lat1*pi/180
    lon2 = lon2*pi/180
    lat2 = lat2*pi/180

    dLon = lon2 - lon1
    y = sin(dLon)*cos(lat2)
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon)
    brng = atan2(y, x)*180/pi

    return(brng)

def dist(y1, x1, y2, x2):
    #print(x1, y1, x2, y2)
    return(calc.distance([y1, x1], [y2, x2]))
#    return(sqrt((x1 - x2)**2 + (y2 - y1)**2))

def speed(a_off_wind):
    if(a_off_wind < pi/6 or a_off_wind > 11*pi/6):
	return(.00001)

    return(sin(a_off_wind / 2) - min(a_off_wind / 2, pi - a_off_wind / 2) * .5 + .00001)

def turn_time(h1, h2):
    turnAngle = min((h1 - h2)%(2*pi), (h2 - h1)%(2*pi))
    return(sin(turnAngle/2)*3)

def total_time(lat_s, lon_s, a_s, lat, lon, lat_e, lon_e, wind_heading):
#    return(x*x*x*x + y*y*y*y*1.7)

    a_s = (a_s*pi/180)%(2*pi)

    d1 = dist(lat_s, lon_s, lat, lon)
    a1 = ((angleFromNorth(lat_s, lon_s, lat, lon))*pi/180)%(2*pi)
    a1OffWind = ((angleFromNorth(lat_s, lon_s, lat, lon) - wind_heading)*pi/180)%(2*pi)

    d2 = dist(lat, lon, lat_e, lon_e)
    a2 = ((angleFromNorth(lat, lon, lat_e, lon_e))*pi/180)%(2*pi)
    a2OffWind = ((angleFromNorth(lat, lon, lat_e, lon_e) - wind_heading)*pi/180)%(2*pi)

    t1 = d1/speed(a1OffWind)
    t2 = d2/speed(a2OffWind)

#    if(random() < .001):
#	    print(a_s, a1, a2, turn_time(a_s, a1))
    
    total_t = t1 + (t1*t1/9999999) + t2 + (t2*t2/9999999) + turn_time(a_s, a1) + turn_time(a1, a2)
#    total_t = turn_time(a_s, a1)

    return(total_t)

