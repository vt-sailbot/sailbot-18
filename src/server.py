"""
Pretty sure this file isn't used
"""

import socket
from random import *

print("SERVER")

host = ''        # Symbolic name meaning all available interfaces
#host = "192.168.7.2"
port = 12345     # Arbitrary non-privileged port

# make a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

print("made socket: " + str((host , port)))

s.listen(1)
conn, addr = s.accept()

print('Connected by', addr)

curLat = 0;
curLon = 0;
while True:
    curLat += random()/100
    curLon += random()/100
    type = random()
    if(type < .85):
        type = 0
    elif(type < .91):
        type = 1
    elif(type < .94):
        type = 2
    elif(type < .95):
        type = 3
    else:
        type = 4

    outString = str(type) + ';' + str(curLat) + ';' + str(curLon)

    conn.sendall(outString)

    try:
        inData = conn.recv(1024)

        if not inData: break

        print "got back: " + inData

        # conn.sendall("got it")

    except socket.error:
        print "Error Occured."
        break


conn.close()
