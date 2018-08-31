1) Your Python Script writes data you want to send /tmp/sailbot-fifo 

2) Server Reads data from /tmp/sailbot-fifo

3) Server waits for connection from client on TCP port 3232

4) Once client connects, server streams data to client.

Note: server only supports 1 client connection for now


Client simply reads from port 3232, you can use telnet or netcat as clients to test if server is
sending data
