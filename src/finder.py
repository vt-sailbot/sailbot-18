import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while(True):
    time.sleep(.1)

    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (3, 3), 0)

#    cv2.imshow('pristine',frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #purplish red
    lower_red = np.array([168,80,50])
    upper_red = np.array([181,255,230])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    #orangeish red
    lower_red = np.array([0,60,80])
    upper_red = np.array([8,255,230])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    #orange
    lower_red = np.array([0,100,80])
    upper_red = np.array([14,255,230])
    mask3 = cv2.inRange(hsv, lower_red, upper_red)


    mask = cv2.bitwise_or(mask1, mask2, mask3)

#    cv2.imshow("masked", cv2.bitwise_and(frame, frame, mask=mask))

    #mask = cv2.bitwise_not(mask)

#    cv2.imshow("snapped", mask)

    mask2 = mask

    vP = 0
    for i in range(30):
        q = 7
        mask2 = cv2.GaussianBlur(mask2, (q, q), 0)
        mask2 = cv2.inRange(mask2, np.array([253]), np.array([255]))
        #cv2.imshow("cores", cores)
        s = sum(sum(mask2))
        if(s == 0):
            vP = i
            break


    print(vP)
    print("$$$$$$$$")


    for i in range(vP):
        q = 7
        mask = cv2.GaussianBlur(mask, (q, q), 0)
        mask = cv2.inRange(mask, np.array([253]), np.array([255]))

#    cv2.imshow("eroded", mask)

    xC = 0
    yC = 0
    n = 0

#    for y in range(0, len(mask), 1):
#        for x in range(0, len(mask[0]), 1):
#            if(mask[y][x] == 255):
#                xC += x
#                yC += y
#                n += 1

    CM = np.average(mask[:,:3], axis=0, weights=mask)    
    print(CM)

    xC = xC*1.0/n
    yC = yC*1.0/n

    print("%%%%%%%%%%%%%%%%%%%%%%")
    print(xC, yC)

    SIZE_X = 640
    SIZY_Y = 480
    #angle from center to edge
    FOV_X = 60
    FOV_Y = 40

    last_x = -(xC - SIZE_X/2)*(1.0/(SIZE_X/2))*FOV_X

    print(xC - SIZE_X/2)
    print(last_x)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

