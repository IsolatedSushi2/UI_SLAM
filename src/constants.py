import os
from src.camera import CameraParameters

DEFAULT_DATASET_DIRECTORY = os.path.join(os.getcwd(), "data", "rgbd_dataset_freiburg1_360")
DEFAULT_CAMERA_PARAMETERS = CameraParameters(640, 480, 525, 525, 319.5, 239.5, 5000)
MAX_DATA_POINT_AMOUNT = -1
MAX_POINTS_PER_CLOUD_RATIO = 0.1 # if equal to 1 it uses all the points, if equal 0.1 it uses 10% random points

HOME_PAGE_INDEX = 0
VIDEO_PAGE_INDEX = 1
POINT_CLOUD_PAGE_INDEX = 2
CAMERA_PAGE_INDEX = 3
