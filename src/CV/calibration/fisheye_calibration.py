import cv2
import numpy as np
import os
import glob
import pickle

assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'

CHECKERBOARD = (6,9)
subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_FIX_SKEW+cv2.fisheye.CALIB_CHECK_COND
_img_shape = None

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the chess_imgs.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('./calibration/chessboard_imgs/*.png')
#images += glob.glob('./calibration/chessboard_imgs_old/*.png')
print(len(images))

for i, fname in enumerate(images):
    img = cv2.imread(fname)
    if _img_shape == None:
        _img_shape = img.shape[:2]
    else:
        assert _img_shape == img.shape[:2], "All images must share the same size."
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),subpix_criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        # cv2.drawChessboardCorners(img, (7, 6), corners, ret)
        # small = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
        # cv2.imshow('img', small)
        # cv2.waitKey(250)

    print(str(round(float(i+1)/(len(images)) * 100, 1)) + "% Complete") # Percent completion

# Initialize parameters
N_OK = len(objpoints) # Number of valid images
DIMS = _img_shape[::-1] # Image dimensions
camera_matrix = np.zeros((3, 3))
dist = np.zeros((4, 1)) # Distortion coefficients
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

# Calculate calibration
rms, _, _, _, _ = \
    cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        camera_matrix,
        dist,
        rvecs,
        tvecs,
        flags=calibration_flags,
        criteria=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )

# Save the values
with open('./calibration/calibration_vals.pkl', 'wb') as f:
    pickle.dump([DIMS, camera_matrix, dist],f)

print(N_OK, "valid images out of", len(images), "images\n")
print(camera_matrix)
