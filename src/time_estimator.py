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
    """ Calculates angle from the North from two points of latitude and longitude
	
	Keyword Arguments: 
	lat1 -- First latitude
	lon1 -- First longtidue
	lat2 -- Second latitude 
	lon2 -- Second longitude
	
	Returns:
	This function returns an angle in degrees. 

	"""
    lon1 = lon1*pi/180		#use np.radians(lon1) 
    lat1 = lat1*pi/180
    lon2 = lon2*pi/180    
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon)
    brng = atan2(y, x)*180/pi

    return(brng)

def dist(y1, x1, y2, x2):
    """ Calculates distance using distance formula.

        Keyword Arguments: 
        x1 -- An x-coordinate
        y1 -- A y-coordinate
        x2 -- Another x-coordinate
        y2 -- Another y-coordinate

        Returns:
        This function returns the distance between (x1, y1) and (x2, y2) as a double.

        """

def dist(y1, x1, y2, x2):
    """ Calculates distance using distance formula.

	Keyword Arguments: 
	x1-- An x-coordinate
	y1 -- A y-coordinate
	x2 -- Another x-coordinate
	y2 -- Another y-coordinate

	Returns:
	This function returns the distance between (x1, y1) and (x2, y2) as a double.

	"""
    #print(x1, y1, x2, y2)
    return(calc.distance([y1, x1], [y2, x2]))
#    return(sqrt((x1 - x2)**2 + (y2 - y1)**2))

def speed(a_off_wind):
    """ 
        Calculates the speed based on the angle of the wind.

	Keyword Arguments:
	a_off_wind -- angle of the wind in radians

	Returns:
	This functions returns the speed of the ship as a double.

    """
    if(a_off_wind < pi/6 or a_off_wind > 11*pi/6):
        return(.00001)
    
    return(sin(a_off_wind / 2) - min(a_off_wind / 2, pi - a_off_wind / 2) * .5 + .00001)

def turn_time(h1, h2):
    """ Calculates the time for the ship to turn.

	Keyword Arguments:
	h1 -- bearing of the ship
	h2 -- angle from north

	Returns:
	This function returns the time for the ship to turn. 

    """
    turnAngle = min((h1 - h2)%(2*pi), (h2 - h1)%(2*pi))
    return(sin(turnAngle/2)*3)

def total_time(lat_s, lon_s, a_s, lat, lon, lat_e, lon_e, wind_heading):
    """ 
    Estimates the total time the ship goes from the distance and speed. 
	
    Keyword Arguments:
    lat_s -- The latitude of ship 
    lon_s -- The longitude of ship
    a_s -- bearing of the ship
    lat -- The latitude of the waypoint
    lon -- The longitude of the waypoint
    lat_e -- The latitide of the target
    lon_e -- The longitude of the target
    wind_heading -- Wind heading of the ship 
	
    Returns:
    This function returns the time traveled as a double.
    """

#  return(x*x*x*x + y*y*y*y*1.7)

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

