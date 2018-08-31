from transform import four_point_transform
import numpy as np
import argparse
import cv2
# import imutils


def get_edges(image, gray=False):
    if not gray:
        # Convert the image to greyscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur the image
    gray = cv2.GaussianBlur(gray, (15, 15), 0)

    # Find and return the edges
    return cv2.Canny(gray, 25, 150)

def get_thresh(img, gray=False):
    if not gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.GaussianBlur(img, (15, 15), 0)
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

'''
def get_contours(image):
    # Resize the image to be 500 pixels tall to increase performance and accuracy
    # of edge detection
    ratio = image.shape[0] / 500.0
    image = imutils.resize(image, height=500)

    # Gets the edge detected image
    edged_img = get_edges(image)

    # Finds contours
    cnts = cv2.findContours(edged_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Handles fact that OpenCV 2 and 3 return different contour types
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # Sorts the returned contours and returns the top 5 highest area contours.
    # This is done to increase performance
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for contour in cnts:
        # Gets the perimeter and approximates a simplified contour
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(curve=contour, epsilon=.02 * perimeter, closed=True)

        # If our approximated contour has four points, then we can assume that
        # we have found our screen
        if len(approx) == 4:
            print approx + "d"
            return approx
'''
