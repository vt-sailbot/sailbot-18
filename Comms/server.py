#! /usr/bin/python2.7

#python2.7

import socket
import sys
import time

PORT = 4242

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', PORT)
s.bind(server_address)

s.listen(1)

while True:
    print("Waiting for connection")
    connection, connection_address = s.accept()
    print("Connection from address: ", connection_address) 
    try:
        while True:
            connection.send("Arbituary Data\n")
            time.sleep(1)
    except socket.error:
        connection.close()
    
    finally:
        connection.close()

s.close()
