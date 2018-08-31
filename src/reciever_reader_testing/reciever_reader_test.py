import Adafruit_BBIO.ADC as ADC
ADC.setup()
from time import sleep
analogPin="P9_33"
while(1):
        input=ADC.read(analogPin)
        print input
        sleep(.5)
