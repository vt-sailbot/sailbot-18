import cv2
import os
import numpy as np


def imshow_split(img1, img2, title="Split Image", height=False):
    """ Shows two images side-by-side in an imshow window.

    Keyword arguments:
    img1 -- The first image
    img2 -- The second image
    title -- The title for the window pane
    ratio -- The aspect ratio to display the images at (default 1)
    """
    if len(img1.shape) != len(img2.shape):
        if len(img1.shape) < len(img2.shape):
            img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        else:
            img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    if type(height) is int:
        aspect_ratio = height / img1.shape[0]
        img1 = cv2.resize(img1, (0, 0), fx=aspect_ratio, fy=aspect_ratio)
        img2 = cv2.resize(img2, (0, 0), fx=aspect_ratio, fy=aspect_ratio)
    cv2.imshow(title, np.hstack((img1, img2)))


def morph_open(mask, d_iters=2, e_iters=2, kernel_size=7):
    """ Applies a morphological opening to a mask.
    Through eroding and then dilating an image, the smaller noise is removed and
    the larger blobs maintain their size. A standard opening has an equal number
    of dilations as erosions.

    Keyword arguments:
    mask -- The binary image to apply the opening to
    d_iters -- The number of dilation iterations (default 2)
    e_iters -- The number of erosion iterations (default 2)
    kernel_size -- The size of the kernel. Only use odd numbers. (default 7)
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    img_erosion = cv2.erode(mask, kernel, iterations=e_iters)
    return cv2.dilate(img_erosion, kernel, iterations=d_iters)


    def color_isolate(img):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        lab = cv2.GaussianBlur(lab,(15,15),0)

        no_lb = lab.copy()
        no_lb[:,:,0] = 0
        no_lb[:,:,2] = 0

        # gray_lb = cv2.cvtColor(no_lb, cv2.COLOR_LAB2BGR)
        gray_lb = cv2.cvtColor(no_lb, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray_lb,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        morphed = morph_open(thresh)
        imshow_split(gray_lb, thresh,height=200)
        cv2.waitKey(0)

def find_buoy(img, draw_result=False, window_title="Buoy", circ_thresh=0.83):
    """ Computes the center and width of the buoy in an image.
    The method applies a hsv mask of shades of red to the image, then computes
    the largest contour in that mask which the algorithm assumes to be the buoy.
    The algorithm then computes the center of the contour and the width of its
    bounding box.

    Keyword arguments:
    img -- An image containing a buoy
    draw_result -- Whether or not to display the contours and center (default False)
    window_title -- The title of the resulting window (default "Center")
    circ_thresh -- The threshold for the ratio between the contour's circum and
                   it's prediected circum (default 0.83)

    Returns:
    center -- A tuple containing the x and y coords of the center of the buoy
    width -- The width of the buoy's bounding box
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (15, 15), 0)

    # Since HSV is circular and red is at 0, we need two masks to get all the
    # shades of red that the buoy might be
    RED_ORANGE_MIN = np.array([0, 150, 150])
    RED_ORANGE_MAX = np.array([15, 255, 255])
    PURPLE_RED_MIN = np.array([160, 100, 100])
    PURPLE_RED_MAX = np.array([180, 255, 255])

    # Calculates the hsv mask
    orange_red_mask = cv2.inRange(hsv, RED_ORANGE_MIN, RED_ORANGE_MAX)
    purpe_red_mask = cv2.inRange(hsv, PURPLE_RED_MIN, PURPLE_RED_MAX)
    mask = orange_red_mask + purpe_red_mask

    # Sets d_iters to 3 to help connect blobs
    kernel = np.ones((7, 7), np.uint8)
    opened_mask = cv2.dilate(mask, kernel, iterations=3)

    # Finds the largest contour
    _, cnts, _ = cv2.findContours(opened_mask.copy(), cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0:
        print('No contours found!')
        if draw_result:
            imshow_split(opened_mask, img, title=window_title, height=200)
            cv2.waitKey(0)
        return None, None

    cnt = max(cnts, key=cv2.contourArea)
    # TODO: BETTER SORTING
    cnt = cv2.convexHull(cnt)

    # Computes the center of the contour
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        print('No moments found!')
        if draw_result:
            imshow_split(opened_mask, img, title=window_title, height=200)
            cv2.waitKey(0)
        return None, None

    (x, y), radius = cv2.minEnclosingCircle(cnt)

    # predicted_area = np.pi * radius**2
    # actual_area = cv2.contourArea(cnt)
    # print('Area ratio:',(actual_area/predicted_area))

    predicted_cicrum = np.pi * radius * 2
    actual_circum = cv2.arcLength(cnt,True)
    circularity = actual_circum / predicted_cicrum
    #print('Circum ratio:', circularity)
    #print()
    if circularity < circularity_thresh:
        return None, None

    # Gets the bounding rect
    _,_,w,h = cv2.boundingRect(cnt)

    if draw_result:
        draw_cnts = img.copy()

        # draw the contour and center of the shape on the image
        cv2.drawContours(draw_cnts, [cnt], -1, (0, 255, 0), 3)
        cv2.circle(draw_cnts, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(draw_cnts, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.circle(draw_cnts,(int(x),int(y)),int(radius), (0,0,255),2)
        # cv2.rectangle(draw_cnts,(x,y),(x+w,y+h),(0,0,255),3)

        # Resize and display the images
        imshow_split(img, draw_cnts, title=window_title, height=200)
        # aspect_ratio = 200 / draw_cnts.shape[0]
        # draw_cnts = cv2.resize(draw_cnts, (0, 0), fx=aspect_ratio, fy=aspect_ratio)
        # cv2.imshow(window_title, draw_cnts)
        cv2.waitKey(0)

    return (cX, cY), cv2.minAreaRect(cnt)

def thresh_detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray.shape, img.shape)
    edges = cv2.Canny(img,100,200)

    imshow_split(img, edges, "side", 300)
    cv2.waitKey(0)

def buoy_distance(pixel_width, focal_length, ACTUAL_WIDTH=0.4):
    """ Calculates the distance of the buoy from the boat.
    The algorithm uses the similar triangles in the following equation:
    (focal_len / pixel_width) = (actual_distance / actual_width)

    Keyword arguments:
    pixel_width -- The width of the buoy in pixels
    focal_length -- The focal length of the camera in pixels
    ACTUAL_WIDTH -- The actual width of the buoy in desired units (default 0.4m)

    Returns:
    distance -- The distance of the buoy in the units of the ACTUAL_WIDTH
    """
    return focal_length * ACTUAL_WIDTH / pixel_width

def angle_from_center(buoy_x, img_width, focal_length):
    """ Calculates the angle of the buoy from the center of the image.
    Uses trig

    Keyword arguments:
    buoy_x - The x coordinate of the center of the buoy
    img_width -- The total width of the image
    focal_length -- The focal length of the camera in pixels

    Returns:
    Offset angle -- The angle offset from the center of the image in degrees
    """
    return np.degrees(np.arctan((buoy_x - img_width/2) / focal_length))
