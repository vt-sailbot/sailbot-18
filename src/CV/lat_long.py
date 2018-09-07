from math import radians, cos, sin, asin, sqrt, atan2, degrees


def haversine(coord1, coord2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    R = 6378100 # Radius of earth in meters

    # convert decimal degrees to radians
    dlat = radians(coord2[0] - coord1[0])
    dlon = radians(coord2[1] - coord1[1])
    lat1 = radians(coord1[0])
    lat2 = radians(coord2[0])

    # haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    return c * R

def compute_offset(distance, bearing, coord1):
    R = 6378100  # Radius of earth in meters
    bearing = radians(bearing)

    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])

    lat2 = asin(sin(lat1) * cos(distance / R) + cos(lat1) * sin(distance / R) * cos(bearing))
    lon2 = lon1 + atan2(
        sin(bearing) * sin(distance / R) * cos(lat1),
        cos(distance / R) - sin(lat1) * sin(lat2))

    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    return lat2, lon2

import geopy
import geopy.distance

# Define starting point.
start = geopy.Point(48.853, 2.349)

# Define a general distance object, initialized with a distance of 1 km.
d = geopy.distance.VincentyDistance(meters = 1)

# Use the `destination` method with a bearing of 0 degrees (which is north)
# in order to go from point `start` 1 km to north.
print(d.destination(point=start, bearing=0).)

print(compute_offset(1, 0, (48.853, 2.349)))

chi = [41.850033,-87.650055]
nyc = [40.714268,-74.005974]
print(haversine(chi,nyc))
# https://www.movable-type.co.uk/scripts/latlong.html
