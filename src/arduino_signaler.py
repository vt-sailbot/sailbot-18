import serial
import time
import ship_data

arduino_port = None
cur_input = ""

old_RC_inputs = []

print_sent_signals = False
print_received_signals = True

def setup():
	global arduino_port
	                                       #???????
	arduino_port = serial.Serial( port="/dev/ttyACM0",
		baudrate=115200,
		timeout=10 )

	arduino_port.open()

def clean(str):
	outStr = ""
	for i in range(len(str)):
		if(str[i] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@$%^&*()_+-=`~{}[]\|;:\'\\,./<>?\"\#"):
			outStr += str[i]
	
	return(outStr)

#read in PWM values
def read_arduino():
	global cur_input, old_RC_inputs

#	print("reading " + str(arduino_port.inWaiting()))

	input = arduino_port.read(arduino_port.inWaiting())
#	print(input)

	RC_inputs = []

	for c in input:
#		print(c, ord(c))

		if(c != '\n'):
			cur_input += c
		else:	
#			print(cur_input)
			values = clean(cur_input).split(';')
			values = [v for v in values if len(v) > 0]
			
			#if there are all 4 RC inputs
			if(len(values) == 4):
				#rudder, sail, auto_switch, other_switch
				RC_inputs = [float(v) for v in values]
#				print(RC_inputs)
			else:
				if(print_received_signals or ("Beaglebone" not in cur_input)):
					print("\ngot: " + cur_input + "\n")

			cur_input = ""

	#if the Beaglebone got new RC inputs, return them
	if(len(RC_inputs) == 4):
		old_RC_inputs = RC_inputs

		if(print_received_signals):
				print("changing RC inputs to " + str(RC_inputs))
		
		return RC_inputs

	#otherwise just return the old ones
	else:
		return old_RC_inputs

#send Arduino desired angles, offset so correct
def write_arduino(left_rudder_angle, right_rudder_angle, sail_winch_angle):
	#ADD 90 TO ANGLES SO THEY FIT INTO BYTES
	lR = int(round(left_rudder_angle)) + 90
	rR = int(round(right_rudder_angle)) + 90
	w = int(round(sail_winch_angle))
	if(w < 0):
		w = 0
	if(w > 180):
		w = 180

	if(print_sent_signals):
		print("sending " + str([250, lR, 251, rR, 252, w]))

	#250 - flag for left rudder angle
	#251 - flag for right rudder angle
	#252 - flag for winch angle
	message = bytearray([250, lR, 251, rR, 252, w])

	arduino_port.write(message)



if(__name__ == '__main__'):

	setup()
	arduino_port.read(arduino_port.inWaiting())

	i = 0
	while(True):
		write_arduino(i, i + 1, i*2)
		print("\n		i = " + str(i))

		time.sleep(1)

		input = arduino_port.read(arduino_port.inWaiting())
		print("\n" + str(input))
		
		i += 1
		time.sleep(1)
