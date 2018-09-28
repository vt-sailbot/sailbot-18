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
    """
    Get status package containing boat status information from ship_data module... Set status vars in ship_data and call status package to receive dictionary... sends status package message to all server addresses defined by 'server_addresses' list 
    
    KWargs:
    n/a

    Reutrns:
    This function does not return any value

    Side Effects:
    Sends message to all addresses on server address list

    Dependent on:
    ship_data.py

    """
    message = str(ship_data.status_package())

    # Send data
#    print('sending "%s"' % message)
    for server_address in server_addresses:
	    sock.sendto(message.encode(), server_address)		#may want to connect to sockets before hand then call socket.send instead ... especially if server addresses are static

if(__name__ == "__main__"):		#used to test send_update method
	for i in range(10000):
		r = random.random()
		ship_data.boat_lat = i*.0001*(.1 + math.sin(r - .5))
		ship_data.boat_lon = i*.0001*(.1 +  math.cos(r - .5))
		ship_data.boat_heading = 90 - r*180/math.pi
		send_update()
		time.sleep(1)


