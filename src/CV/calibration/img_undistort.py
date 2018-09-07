import cv2
import pickle
import os
import numpy as np

# All this to include camera.py
from os.path import dirname, abspath
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from camera import Camera

path = "./calibration/chessboard_imgs/";
imgs = os.listdir(path)
cam = Camera(disable_video=True, calibration_path="./calibration/calibration_vals.pkl")
for fname in imgs:
    img = cv2.imread(path + fname)
    if img is not None:
        img = cam.undistort(img)
        small = cv2.resize(img, (0,0), fx=0.6, fy=0.6)
        cv2.imshow(fname, small)
        cv2.waitKey(0)
