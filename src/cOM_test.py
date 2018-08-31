import cv2
import numpy as np
import time
import math

show_steps = False

xA = 0

#find the com of the final blob
scale_factor = .17
SIZE_X = 1920*scale_factor
SIZE_Y = 1080*scale_factor
#angle from center to edge
FOV_X = 60
FOV_Y = 40

cam = cv2.VideoCapture(0)

def react_to_buoy(xC, yC, area):

    global xA

    xA = -(xC - SIZE_X/2)*(1.0/(SIZE_X/2))*FOV_X
    yA = -(yC - SIZE_Y/2)*(1.0/(SIZE_Y/2))*FOV_Y


    #heel_angle = ship_data.boat_roll
    #new_xA = xA*math.cos(heel_angle*math.pi/180) - xA*math.sin(heel_angle*math.pi/180)

    print("%%%%%%%%%%%%%%%%%%%%% orange-red at %%%%%%%%%%%%%%%%%%%%%%%%")
    print(xA, yA)
    print("reacted")

def get_mask(frame):
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    if(show_steps):
        cv2.imshow('pristine',frame)
        cv2.waitKey(0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    print(hsv[0][0])

    #purplish red
    lower_red = np.array([168,80,50])
    upper_red = np.array([181,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    #orangeish red
    lower_red = np.array([0,60,80])
    upper_red = np.array([9,255,255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    #orange
    lower_red = np.array([0,100,80])
    upper_red = np.array([14,255,255])
    mask3 = cv2.inRange(hsv, lower_red, upper_red)


    mask = cv2.bitwise_or(cv2.bitwise_or(mask1, mask2), mask3)

    return mask

def get_com(mask):
    maskToErode = mask.copy()

    vP = 0
    for i in range(30):
        q = 5
        maskToErode = cv2.GaussianBlur(maskToErode, (q, q), 0)
        maskToErode = cv2.inRange(maskToErode, np.array([253]), np.array([255]))
        s = sum(sum(maskToErode))

        if(s == 0):
            vP = i
            break

    maskToErode = mask.copy()
    for i in range(vP):
        if(show_steps):
            cv2.imshow("eroded", maskToErode)
            cv2.waitKey(0)

        q = 5
        maskToErode = cv2.GaussianBlur(maskToErode, (q, q), 0)
        maskToErode = cv2.inRange(maskToErode, np.array([253]), np.array([255]))


    if(show_steps):
        cv2.imshow("eroded", maskToErode)
        cv2.waitKey(0)

    ms = cv2.moments(maskToErode)
#    print(ms)

    xC = (ms['m10']/ms['m00'])
    yC = (ms['m01']/ms['m00'])

    return(xC, yC)

def get_circularity_and_area(mask, xC, yC):
    if(show_steps):
        cv2.imshow("masked", mask)
        cv2.waitKey(0)

    time.sleep(.5)

    h, w = mask.shape[:2]
    blank_mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(mask, blank_mask, ((int)(xC), (int)(yC)), 181)

    if(show_steps):
        cv2.imshow("filled", mask)
        cv2.waitKey(0)

    frame = cv2.inRange(mask, np.array(170), np.array(190))
    if(show_steps):
        cv2.imshow("isolated", frame)
        cv2.waitKey(0)

    cv2.imwrite("isolated.png", frame)

    area = cv2.moments(frame)['m00']/255.0

    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.inRange(frame, np.array(100), np.array(200))
    if(show_steps):
        cv2.imshow("edge", frame)
        cv2.waitKey(0)

    perimeter = cv2.moments(frame)['m00']/255.0
    print(area, perimeter)

    perimeter_if_blob_were_circular = (math.sqrt(area/math.pi)*2*math.pi)*(2.0/3)

    print(perimeter_if_blob_were_circular)

    return(perimeter/perimeter_if_blob_were_circular, area)


# Capture frame-by-frame
#ret, frame = cap.read()

def check_camera():
#	frame = cv2.imread("test_mask.png")
#	ret, frame = cam.read()
	ret, frame = cam.read()
	for i in range(3):
		ret, frame = cam.read()

	frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)

	cv2.imwrite("read.png", frame)
	
	mask = get_mask(frame)
	(xC, yC) = get_com(mask)
	
	time.sleep(.5)
	
	circularity, area = get_circularity_and_area(mask, xC, yC)
	
	print(circularity)
        print(xC, yC, area)
	print("----------------------------------")
	
	if(circularity < 2):
	    print("CIRCULAR")
	
	    react_to_buoy(xC, yC, area)
