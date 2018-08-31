import random
import time


filename = "/tmp/sailbot-fifo"


while (1):
    time.sleep(1)
    
    file = open(filename, "a+")
    
    val1 = random.random()
    packet = "[" + str(val1) +  "]\n"
    print("Writing packet to socket: " + packet )
    file.write(packet)
    
    file.close()
            
