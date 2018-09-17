import cv2
import numpy as np
import time

time_of_last_id = 0
last_x = 0
last_y = 0
last_size = 10

"""			commented out this section ... not valid python statements ... also var names are not consistent with rest of codebase
SIZE_X = 
SIZE_Y = 
#angle from center to edge
FOV_X = 
FOV_Y = 
"""
#read camera		should there be something here? perhaps declaring 'keypoint' list

#find largest red blob

centers = [p.pt for p in keypoints]
sizes = [p.size for p in keypoints]
maxI = 0

for p in keypoints:
    print(p.pt)
    print(p.size)


#put the following in a method
if(len(keypoints) > 0):
	biggest_blob_i = sizes.index(max(sizes))
	center = keypoints[biggest_blob_i].pt

	last_x = (center[0] - SIZE_X/2)*(FOV_X*1.0/SIZE_X/2)
	last_y = (center[1] - SIZE_Y/2)*(FOV_Y*1.0/SIZE_Y/2)
	last_size = keypoints[biggest_blob_i].size
	time_of_last_id = time.time()

	#assuming boat's level
	bH = ship_data.boat_heading
	buoyH = (last_x + bH)%360

	print("biggest point: ")
	print(sizes.index(max(sizes)))
	print(keypoints[biggest_blob_i].pt)
	print(keypoints[biggest_blob_i].size)

