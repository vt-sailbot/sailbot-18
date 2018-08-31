import ship_data
import captain
import servo


# Wind angles that make the sail fully-in and sail fully-out
sail_in_wind_angle = 60
sail_out_wind_angle = 120

# Winch servo fully-out and fully-in values
# SAILS FULLY IN
winch_min = 90
# FULLY OUT
winch_max = 150

# Rudder servo fully-left and fully-right values
rudder_min = -45
rudder_max = 45

class Helmsman:

    def __init__(self, cap):
        self.captain = cap

	self.target_rudder_angle = 0
	self.target_winch_angle = 60

    def setup(self):
	q = None

    def fit_into_range(self, x, x_min, x_max):
        if(x < x_min):
            return x_min
        if(x > x_max):
            return x_max
        return x

    # turns the rudder based on where the servo should go
    def setRudderAngleFromcDH(self, target_heading):
        current_heading = ship_data.boat_heading
        angle_to_turn = (target_heading - current_heading)%360
	
	if(angle_to_turn > 180):
		angle_to_turn -= 360


	self.target_rudder_angle = self.fit_into_range(angle_to_turn/1.2, rudder_min, rudder_max)

    # turns the sail winch based on the current wind direction
    def setWinchAngleFromWind(self):
	relative_wind_angle = ship_data.relative_wind_heading
	if(relative_wind_angle > 180):
		relative_wind_angle = 360 - relative_wind_angle
        wind_angle_ratio = (relative_wind_angle - sail_in_wind_angle)*1.0/(sail_out_wind_angle - sail_in_wind_angle)

        if(wind_angle_ratio > 1):
            wind_angle_ratio = 1
        if(wind_angle_ratio < 0):
            wind_angle_ratio = 0

        # update target winch angle							
        self.target_winch_angle  = winch_min + (winch_max - winch_min) * wind_angle_ratio


    def steer_boat(self):
        # If the boat's automatic, follow the captain's current desired heading
        if(ship_data.auto):
            self.setRudderAngleFromcDH(self.captain.current_desired_heading)
            self.setWinchAngleFromWind()

        # Otherwise, blindly follow the RC input
        else:
    		self.target_rudder_angle = ship_data.RC_rudder_angle
	    	self.target_winch_angle = ship_data.RC_winch_angle

	ship_data.target_rudder_angle = self.target_rudder_angle
	ship_data.target_winch_angle = self.target_winch_angle

