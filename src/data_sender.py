import time
import socket
import sys
import math
import random
#import main

import ship_data
import captain

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind(('localhost', 7777))

server_addresses = [('192.168.0.100', 10101), ('192.168.0.101', 10101), ('192.168.0.102', 10101), ('192.168.0.103', 10101), ('192.168.0.104', 10101)]
#sock.connect(server_address)

def send_update():
    message = str(ship_data.status_package())

    # Send data
#    print('sending "%s"' % message)
    for server_address in server_addresses:
	    sock.sendto(message.encode(), server_address)

if(__name__ == "__main__"):
	for i in range(10000):
		r = random.random()
		ship_data.boat_lat = i*.0001*(.1 + math.sin(r - .5))
		ship_data.boat_lon = i*.0001*(.1 +  math.cos(r - .5))
		ship_data.boat_heading = 90 - r*180/math.pi
		send_update()
		time.sleep(1)


