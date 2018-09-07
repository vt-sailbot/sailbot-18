import numpy as np
import cv2
import buoy_cv as bcv
from camera import Camera

def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 35, 125)

    # Gets contours
    _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Finds the most rectangular of the 10 largest contours
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    paperCnt = None
    for cnt in cnts:
        # Simplify the contour
        peri = cv2.arcLength(cnt, True)
        simple = cv2.approxPolyDP(cnt, peri * .02, True)

        # if the simplified shape has 4 corners, we can assume it's the paper
        if len(simple) == 4:
            paperCnt = simple
            break

    # Computes the center of the contour
    M = cv2.moments(paperCnt)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        return (None, None), None

    # compute the bounding box of the of the paper region and return it along
    # with the center
    return (cX, cY), cv2.minAreaRect(paperCnt)

cam = Camera(video_channel=1)
ACTUAL_WIDTH = 24 # in
while True:
    image = cam.get_frame(mirrored=1, undistorted=True)
    center, marker = bcv.find_buoy(image)
    if marker is not None and center is not None:
        (cX, cY) = center
        buoy_width = marker[1][0]

        inches = bcv.buoy_distance(buoy_width, cam.FOCAL_LEN_X, ACTUAL_WIDTH)
        angle = bcv.angle_from_center(cX, cam.IMG_WIDTH, cam.FOCAL_LEN_X)
        se
        # Draw a bounding box around the contour
        box = np.int0(cv2.boxPoints(marker))
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

        # Draw the center
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(image, "%.2fft : %i degrees" % (inches / 12, angle), (cX - 20, cY - 20),
                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # # Display the length
        # cv2.putText(image, "%.2fft" % (inches / 12),
        # (cam.IMG_WIDTH - 250, cam.IMG_HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX,
        # 2.0, (0, 255, 0), 3)
        #
        # # Display the angle
        # cv2.putText(image, "%ideg" % angle,
        # (cam.IMG_WIDTH - 300, cam.IMG_HEIGHT - 80), cv2.FONT_HERSHEY_SIMPLEX,
        # 2.0, (0, 255, 0), 3)

    cv2.imshow("image", cv2.resize(image, (0, 0), fx=.5, fy=.5))
    cv2.waitKey(1)
