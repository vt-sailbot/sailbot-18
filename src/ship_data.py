# How close the boat needs to approach targets
POINT_PROXIMITY_RADIUS = 9

# The minimum angle off upwind the boat should sail
TACK_ANGLE = 45
# The minimum angle off downwind the boat should sail
GYBE_ANGLE = 20

start_time = 0

RC_winch_angle = 60
RC_rudder_angle = 0

target_rudder_angle = 0
target_winch_angle = 0

auto = False
auto_start_time = -7
other = False

boat_heading = 0
boat_speed = 0

relative_wind_heading = 0
wind_heading = 0
wind_speed = 0

boat_roll = 0
boat_pitch = 0
boat_yaw = 0

boat_lat = 0
boat_lon = -10

# Which target is next
targetI = 0

current_distance_to_target = 10101
direction_to_target = 0

# List of target points in order
target_points = [(37.231502, -80.421209)]

# The Captain's current target midpoint and current desired heading
current_fastest_midpoint = None
current_desired_heading = None
current_fastest_time_to_target = None

def status_package():
        """
        Makes dictionary called package with status information on boat ... called by data_sender
	
        KWargs:
        n/a

        Returns:
        Dictionary 'package' of ship data

        """
        package = {};   	#may want to consider replacing with structured numpy array ... more versatile, faster operations ... drawback is need to use pickling before sending over socket

        package["boat_lat"] = boat_lat
        package["boat_lon"] = boat_lon
        package["wind_heading"] = wind_heading
        package["wind_speed"] = wind_speed
        package["boat_heading"] = boat_heading
        package["boat_speed"] = boat_speed
        package["RC_rudder_angle"] = RC_rudder_angle
        package["RC_winch_angle"] = RC_winch_angle
        package["rudder_angle"] = target_rudder_angle
        package["winch_angle"] = target_winch_angle
        package["target_waypoint"] = target_points[targetI]
        package["current_fastest_midpoint"] = current_fastest_midpoint
        package["current_desired_heading"] = current_desired_heading
        package["current_fastest_time_to_target"] = current_fastest_time_to_target
        return(package)
