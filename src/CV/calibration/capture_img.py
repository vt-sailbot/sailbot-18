import random
import cv2
import time

# All this to include camera.py
from os.path import dirname, abspath
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from camera import Camera

cam = Camera(video_channel=1, calibration_path="./calibration/calibration_vals.pkl")
start = time.time()
count = 1
num_imgs = 3
freq = .5 # Hz
while True:
    img = cam.get_frame(undistorted=True)
    small = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
    cv2.imshow('my webcam', small)
    cv2.waitKey(1)
    if time.time() - start > 1/freq:
        print ('img captur ied ' + str(count))
        cv2.imwrite('./calibration/sample_imgs/' + str(random.randint(0, 99999)) + '.png', img)
        start = time.time()
        count += 1
        if count > num_imgs:
            break;
    cv2.destroyAllWindows()
