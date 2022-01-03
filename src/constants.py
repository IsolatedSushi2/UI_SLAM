import os
from src.camera import CameraParameters
import cv2

# Dataset parameters
DEFAULT_DATASET_DIRECTORY = os.path.join(
    os.getcwd(), "dataTUM", "rgbd_dataset_freiburg1_360")
DEFAULT_CAMERA_PARAMETERS = CameraParameters(
    640, 480, 525, 525, 319.5, 239.5, 5000)

MAX_DATA_POINT_AMOUNT = 40  # Use -1 if you want to use all the points

# Image parameters
# Whether to keep all the images in memory for displaying them in the video page (memory intensive)
STORE_ALL_IMAGES = True
DRAW_KEYPOINTS_MATCHES = True  # Whether to render the keypoints and matches aswell

# Pointcloud parameters
# TODO Not usefull to take every pointCloud, reduce the amount
POINTCLOUD_INCREMENT_AMOUNT = 1
# if equal to 1 it uses all the points, if equal 0.1 it uses 10% random points
MAX_POINTS_PER_CLOUD_RATIO = 0.01

# Algorithm parameters
MAX_MATCH_AMOUNT = 50  # For matching the keypoints
KEYPOINT_FINDER = cv2.ORB_create(nfeatures=1000)
MATCHING_ALG = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) #  TODO play with crossCheck value

# UI parameters
HOME_PAGE_INDEX = 0
VIDEO_PAGE_INDEX = 1
POINT_CLOUD_PAGE_INDEX = 2
CAMERA_PAGE_INDEX = 3
CHARTS_PAGE_INDEX = 4