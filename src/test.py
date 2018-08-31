import time_estimator

a_s = 3#ship_data.boat_heading
lon_s = 0#ship_data.boat_lon
lat_s = 0#ship_data.boat_lat

lon_e = 0#self.current_target[1]
lat_e = .01#self.current_target[0]
a_e = 0

wind_heading = 0#ship_data.wind_heading


def T(x):
    lat = x[0]
    lon = x[1]
    return(time_estimator.total_time(lat_s, lon_s, a_s, lat, lon, lat_e, lon_e, wind_heading))

print(T([.005, .006]))
