import cv2
import pickle

# All this to include camera.py
from os.path import dirname, abspath
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from camera import Camera

print("Press q to quit")
cam = Camera(video_channel=1, calibration_path="./calibration/calibration_vals.pkl")
while True:
    img = cam.get_frame(mirrored=True, undistorted=True)
    if img is not False:
        small = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('my webcam', small)
        if cv2.waitKey(1) == ord('q'):
            break  # esc to quit
        cv2.destroyAllWindows()
