import cv2
import numpy as np
import buoy_cv as bcv
from camera import Camera
import os

# Grabs and shuffles the images
data_path = "./data/"
img_dir = os.listdir(data_path)
img_dir = [im for im in img_dir if '.png' in im or '.jpg' in im]
#np.random.shuffle(img_dir)

# img = cv2.imread(data_path + "backg1.jpg")
# center, width = bcv.get_buoy_size(img, True, "backg")

cam = Camera(disable_video=True)

for img_path in img_dir:
    img = cv2.imread(data_path + img_path)
    # img = cam.undistort(img)
    # center, px_width = bcv.get_buoy_size(img, True, img_path)
    # if center is not None:
    #     distance = bcv.buoy_distance(px_width, cam.FOCAL_LEN_X)
    #     angle_from_center = bcv.angle_from_center(center[0], cam.DIMENSIONS[0], cam.FOCAL_LEN_X)

    #bcv.color_isolate(img)
    bcv.find_buoy(img, draw_result=True)
