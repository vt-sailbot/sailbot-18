from transform import four_point_transform, self_transform
from scan import *
import numpy as np
import cv2
from pprint import pprint


def mos_pos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        cv2.circle(param[0], (x, y), 10, (0, 255, 0), 2)
        cv2.imshow("img", param[0])
        param[1].append((x, y))


def get_src_corners(image):
    corners = []
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", mos_pos, [image, corners])
    cv2.imshow("img", image)

    print "Select four corners then press any button to continue"

    while (len(corners) < 4):
        cv2.waitKey(1000)

    return np.asarray(corners, dtype="float32")


path = './maze1.jpg'
image = cv2.imread(path)

# Gets coordinates of coordinates
#corners = get_src_corners(image.copy())
corners = np.array([[227., 342.],
                    [483., 345.],
                    [492., 537.],
                    [206., 538.]])
# cv2.destroyWindow("img")

warped = four_point_transform(image, corners)
# unwarped = four_point_transform(warped, corners, True)
#my_warped = self_transform(image, corners)

#edges = get_edges(warped)
#thresh = get_thresh(warped)

#backwards = four_point_transform(warped, corners)

cv2.imwrite("warped.jpg", warped)
# cv2.imshow("Warped", warped)
# cv2.imshow("Un Warped", unwarped)
#cv2.imshow("Edges", edges)
#cv2.imshow("Thresh", thresh)

# write_matrix_file(thresh, 'mout.txt')
#write_csv(thresh, "thresh.csv")
#s = SolveMaze(thresh)

cv2.waitKey(0)
