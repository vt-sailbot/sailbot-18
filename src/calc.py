import math
import ship_data
#import point

class Point:
    """ Holds latitudes and longitudes for a single point
    """
    lat = 0
    lon = 0

    def __init__(self, lat_and_lon):
        """Initializes the latitudes and longitudes of the point

        Keyword arguments:
        self -- The caller, Point instance
        lat_and_lon -- array of with latitude at 0 index and longitude at 1 index

        Side effects:
        -Initializes instance variables
        """
        self.lat = lat_and_lon[0]
        self.lon = lat_and_lon[1]

    def __str__(self):
        """ Returns a String with the latitude and longitude

        Keyword arguments:
        self -- The caller, the instance

        Returns:
        This function returns a String with the coordinates
        """
        return str((self.lat, self.lon))

def direction_to_point(current_point, target_point):
    """ Function to determine the direction between the current point and the
    target point.

    Keyword arguments:
    current_point -- An array with coordinates of the current point
    target_point -- An array with coordinates of the target point

    Returns:
    This function returns an angle in degrees
    """
    a = math.radians(current_point[0])
    b = math.radians(target_point[0])
    d = math.radians(target_point[1] - current_point[1])

    y = math.sin(d) * math.cos(b)
    x = math.cos(a) * math.sin(b) - math.sin(a) * math.cos(b) * math.cos(d)


    return (math.degrees(math.atan2(y, x)) + 360) % 360

def get_heading_angle(heading, current_point, target_point):
    """ Gets the heading angle to the target point from the curretn pointself.

    Keyword arguments:
    heading -- Angle in degrees of current heading
    current_point -- Array that has the coordinates of the current point
    target_point -- Array that has the coordinates of the target point

    Returns:
    An angle that is the direction to point subtracted from the current heading
    """
    angle = direction_to_point(current_point, target_point)

    return heading - angle

def within_radius_of_target(current_point, target_point):
    """ Returns if the current_point is within a given distance of the target_point

    Keyword arguments:
    current_point -- An array with coordinates of the current point
    target_point -- An array with coordinates of the target point

    Returns:
    Boolean if the current point is within a given distance of the target point

    """
    return (distance(current_point, target_point) <= ship_data.POINT_PROXIMITY_RADIUS)

def distance(point1, point2):
    """ Calclates the distance between the two point

    Keyword arguments:
    point1 -- An array with coordinates of a point
    point2 -- An array with coordinates of a second point

    Returns:
    A distance between the two points
    """
    a = math.sin(math.radians(point1[0]))
    b = math.sin(math.radians(point2[0]))
    c = math.cos(math.radians(point1[0]))
    d = math.cos(math.radians(point2[0]))

    e = a * b + c * d * math.cos((math.radians(point2[1] - point1[1])))
    f = math.acos(e)

    return f * 6371 * 1000
