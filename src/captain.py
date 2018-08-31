import ship_data
import calc
from calc import Point
import minimizer
import time_estimator
import time

class Captain:

    def __init__(self):

        self.current_desired_heading = 0

        #self.current_target = None
        #self.current_position = None

        # -1 -> left tack       0 -> na       1 -> right tack
        self.on_tack = 0
        self.time_on_tack = 0.0

        self.on_gybe = 0
        self.time_on_gybe = 0.0

        self.old_time = time.time()

	self.current_fastest_midpoint = [1, 2];

    def setup(self):
        self.old_time = time.time()
        self.current_target = (ship_data.target_points[ship_data.targetI])

    def think(self):
        a_s = ship_data.boat_heading
        lon_s = ship_data.boat_lon
        lat_s = ship_data.boat_lat

        lon_e = self.current_target[1]
        lat_e = self.current_target[0]
        a_e = 0

        wind_heading = ship_data.wind_heading


        def T(x):
            lat = x[0]
            lon = x[1]
            return(time_estimator.total_time(lat_s, lon_s, a_s, lat, lon, lat_e, lon_e, wind_heading))


        dTotal = calc.distance([lat_s, lon_s], [lat_e, lon_e])/(111*1000.0)

        self.current_fastest_midpoint = minimizer.minimize(T, [(lat_e + lat_s)/2, (lon_e + lon_s)/2], [dTotal/2, dTotal/2], 1, lastMinX=self.current_fastest_midpoint)
	
	#if it's better just to go through the midpoint, do it
	if(T([(lat_s + lat_e)/2, (lon_s + lon_e)/2]) < T(self.current_fastest_midpoint)):
		self.current_fastest_midpoint = [(lat_s + lat_e)/2, (lon_s + lon_e)/2]

	self.current_desired_heading = calc.direction_to_point([ship_data.boat_lat, ship_data.boat_lon], self.current_fastest_midpoint)

	ship_data.current_fastest_midpoint = self.current_fastest_midpoint
	ship_data.current_desired_heading = self.current_desired_heading
	ship_data.current_fastest_time_to_target = T(self.current_fastest_midpoint)

    #    print(self.current_fastest_midpoint)


#        print(minimizer.minimize(T, [(lat_e + lat_s)/2, (lon_e + lon_s)/2], [dTotal/2, dTotal/2], 1, lastMinX=self.current_fastest_midpoint)
#	print(self.current_fastest_midpoint)

if(__name__ == '__main__'):
	c = Captain()
	for i in range(10):
		c.think()
