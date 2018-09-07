import cv2
import pickle
import os
import numpy as np

class Camera:
    def __init__(self, disable_video=False, video_channel=1, calibration_path=False):
        # Load the undistortion parameters
        if calibration_path:
            self.CALIBRATED = True
            with open(calibration_path, 'rb') as f:
                DIMS, camera_matrix, dist = pickle.load(f)
                self.map1, self.map2 = cv2.fisheye.initUndistortRectifyMap(camera_matrix, dist, np.eye(3), camera_matrix, DIMS, cv2.CV_16SC2)

            self.FOCAL_LEN_X = camera_matrix[0][0] # The X focal length
        else:
            self.CALIBRATED = False

        if not disable_video:
            self.video_capture = cv2.VideoCapture(video_channel)
            _, frame = self.video_capture.read()
            self.DIMENSIONS = frame.shape
            self.IMG_WIDTH = self.DIMENSIONS[1]
            self.IMG_HEIGHT = self.DIMENSIONS[0]
        else:
            self.DIMENSIONS = DIMS

        if self.CALIBRATED:
            fov_rad = 2 * np.arctan((self.DIMENSIONS[0]/(2 * self.FOCAL_LEN_X)))
            self.FOV = np.degrees(fov_rad)

    def get_frame(self, mirrored=False, undistorted=False):
        if self.video_capture.isOpened():
            retval, frame = self.video_capture.read()
            if retval:
                if mirrored:
                    frame = cv2.flip(frame, 1)
                if undistorted and self.CALIBRATED:
                    frame = self.undistort(frame)
                return frame
        return False

    def undistort(self, img):
        if not self.CALIBRATED:
            print("NO CALIBRATION PATH PASSED INTO IMAGE. RETURNING BASE IMAGE")
            return img
        return cv2.remap(img, self.map1, self.map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
