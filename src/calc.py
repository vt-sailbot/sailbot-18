import math
import ship_data
#import point

class Point:
    lat = 0
    lon = 0

    def __init__(self, lat_and_lon):
        self.lat = lat_and_lon[0]
        self.lon = lat_and_lon[1]

    def __str__(self):
        return str((self.lat, self.lon))

def direction_to_point(current_point, target_point):
    a = math.radians(current_point[0])
    b = math.radians(target_point[0])
    d = math.radians(target_point[1] - current_point[1])

    y = math.sin(d) * math.cos(b)
    x = math.cos(a) * math.sin(b) - math.sin(a) * math.cos(b) * math.cos(d)


    return (math.degrees(math.atan2(y, x)) + 360) % 360

def get_heading_angle(heading, current_point, target_point):
    angle = direction_to_point(current_point, target_point)

    return heading - angle

def within_radius_of_target(current_point, target_point):
    return (distance(current_point, target_point) <= ship_data.POINT_PROXIMITY_RADIUS)

def distance(point1, point2):
    a = math.sin(math.radians(point1[0]))
    b = math.sin(math.radians(point2[0]))
    c = math.cos(math.radians(point1[0]))
    d = math.cos(math.radians(point2[0]))

    e = a * b + c * d * math.cos((math.radians(point2[1] - point1[1])))
    f = math.acos(e)

    return f * 6371 * 1000

