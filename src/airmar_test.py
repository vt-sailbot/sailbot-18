import airmar_reader
import ship_data
import time
import data_sender

airmar_reader.print_airmar_input = True
airmar_reader.print_airmar_sentence_contents = True
airmar_reader.setup()

while(True):
	airmar_reader.read_airmar()

	print("at: ")
	print(ship_data.boat_lat, ship_data.boat_lon)
#	print("facing: ")
#	print(ship_data.boat_heading)
#	print("\nwind from:")
#	print(ship_data.wind_heading)

	data_sender.send_update()

	time.sleep(1)
