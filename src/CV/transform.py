import cv2
import numpy as np
from pprint import pprint

# Program: transform.py
# Purpose: Outputs a four point perspective transform using OpenCV
#
# David Haas
# 2/12/18


def order_points(pts):
    # Orders a set of coordinates in a 4x2 array such that:
    # 0: top left, 1: top right, 2: bottom left, 3: bottom right

    # initializes an empty 4x2 npy array to store the coordinates
    rect = np.zeros((4, 2), dtype="float32")

    # Sums up each set of coordinate points (x+y)
    s = pts.sum(axis=1)

    # Top left will have the smallest sum, bottom right will have the largest sum
    rect[0] = pts[np.argmin(s)]
    rect[3] = pts[np.argmax(s)]

    # Takes the difference of each set of coordinate points (y-x)
    diff = np.diff(pts, axis=1)

    # Top right will have the smallest diff, bottom left will have largest diff
    rect[1] = pts[np.argmin(diff)]
    rect[2] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, bounds, reverse=False):

    # Ensures that the inputted coordinates are ordered
    bounds = order_points(bounds)

    (tl, tr, bl, br) = bounds

    # Uses distance formula to calculate the distance between the two bottom
    # coordinates. Does the same with two top coordinates.
    width1 = np.sqrt(((br[0] - bl[0])**2) + ((br[1] - bl[1])**2))
    width2 = np.sqrt(((tr[0] - tl[0])**2) + ((tr[1] - tl[1])**2))

    # Finds the larger of the two widths, which will be the width for the new
    # image
    max_width = max(int(width1), int(width2))

    # Does the same for height.
    height1 = np.sqrt(((tr[0] - br[0])**2) + ((tr[1] - br[1])**2))
    height2 = np.sqrt(((tl[0] - bl[0])**2) + ((tl[1] - bl[1])**2))

    # Largest height -> height for new image
    max_height = max(int(height1), int(height2))

    # Uses the calculated dimensions to construct a new array for the top-down
    # birds-eye view for the destination image
    new_dims = np.array(
        [[0, 0], [max_width - 1, 0], [0, max_height - 1],
         [max_width - 1, max_height - 1]],
        dtype="float32")

    #print bounds
    #print new_dims
    # Get perspective transform matrix from the original coords to the new ones
    ptm = cv2.getPerspectiveTransform(bounds, new_dims)
    if reverse:
        return cv2.warpPerspective(
            image,
            ptm, (max_width, max_height),
            borderMode=cv2.BORDER_CONSTANT,
            flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)

    return cv2.warpPerspective(image, ptm, (max_width, max_height))


def find_coeffs(src, dst):
    # https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
    # https://math.stackexchange.com/questions/494238/how-to-compute-homography-matrix-h-from-corresponding-points-2d-2d-planar-homog
    matrix = []
    pprint(src)
    pprint(dst)

    # Combines two sets and turns them into a list of tuples: [(pa[0], pb[0]), ... (pa[n], pb[n])]
    for p1, p2 in zip(src, dst):
        # print p1, p2
        matrix.append(
            [-p1[0], -p1[1], -1, 0, 0, 0, p2[0] * p1[0], p2[0] * p1[1]])
        matrix.append(
            [0, 0, 0, -p1[0], -p1[1], -1, p2[1] * p1[0], p2[1] * p1[1]])
    # print '\nMatrix: '
    # pprint(matrix)

    A = np.matrix(matrix, dtype=np.float)
    #A = A * -1

    B = np.array(dst).reshape(8)
    # print '\nB:'
    # pprint(B)

    # print '\nnp.linalg.inv(A.T * A) * A.T'
    # print(np.linalg.inv(A.T * A) * A.T)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    # print '\nres:'
    # pprint(res)

    ret = np.append(np.array(res).reshape(8), [1])
    ret = ret.reshape((3, 3))

    # print '\nFinal:'
    # pprint(ret)
    return ret


def perspective_map(src, M, dims):
    width, height = dims
    dst = np.zeros((height, width, 3), dtype='uint8')

    for y in range(height):
        for x in range(width):
            #print x,y
            # calc_x = ((M[0, 0] * x + M[0, 1] * y + M[0, 2]) /
            #           (M[2, 0] * x + M[2, 1] * y + M[2, 2]))
            #
            # calc_y = ((M[1, 0] * x + M[1, 1] * y + M[1, 2]) /
            #           (M[2, 0] * x + M[2, 1] * y + M[2, 2]))
            a = x * M[0, 0] + y * M[1, 0] + M[2, 0]
            b = x * M[0, 1] + y * M[1, 1] + M[2, 1]
            c = x * M[0, 2] + y * M[1, 2] + M[2, 2]
            calc_x = a / c
            calc_y = b / c

            calc_x = abs(int(round(calc_x)))
            calc_y = abs(int(round(calc_y)))
            #print x, y, calc_x, calc_y
            dst[y][x] = src[calc_y][calc_x]
    return dst


def self_transform(image, bounds):

    # Ensures that the inputted coordinates are ordered
    bounds = order_points(bounds)

    (tl, tr, bl, br) = bounds

    # Uses distance formula to calculate the distance between the two bottom
    # coordinates. Does the same with two top coordinates.
    width1 = np.sqrt(((br[0] - bl[0])**2) + ((br[1] - bl[1])**2))
    width2 = np.sqrt(((tr[0] - tl[0])**2) + ((tr[1] - tl[1])**2))

    # Finds the larger of the two widths, which will be the width for the new
    # image
    max_width = max(int(width1), int(width2))

    # Does the same for height.
    height1 = np.sqrt(((tr[0] - br[0])**2) + ((tr[1] - br[1])**2))
    height2 = np.sqrt(((tl[0] - bl[0])**2) + ((tl[1] - bl[1])**2))

    # Largest height -> height for new image
    max_height = max(int(height1), int(height2))

    # Uses the calculated dimensions to construct a new array for the top-down
    # birds-eye view for the destination image
    new_dims = np.array(
        [[0, 0], [max_width - 1, 0], [0, max_height - 1],
         [max_width - 1, max_height - 1]],
        dtype="float32")

    #print bounds
    #print new_dims
    # Get perspective transform matrix from the original coords to the new ones
    M = find_coeffs(bounds, new_dims) * -1
    print M

    return perspective_map(image, M, (max_width, max_height))
