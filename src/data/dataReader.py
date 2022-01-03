import os
import numpy as np
import cv2
from PIL import Image
from src.constants import MAX_DATA_POINT_AMOUNT
from src.associate import read_file_list, associate
from src.camera import CameraLocations


# Main dataObject
class Data:
    def __init__(self):
        # String containing the path to the dataset
        self.path = ""

        # List containing timestamps
        self.timestamps = []

        # Dictionaries containing the timestamps and fileNames
        self.rgbFileNames = {}
        self.depthFileNames = {}

        # Dictionaries containing the timestamps and the image
        self.frames = {}
        self.stereoFrames = {}

        # Dictionaries containing the timestamps and ground truth movement relative to origin
        self.trueCamLocs = {}
        self.modeledCamLocs = {}

        # Dictionaries containing the timestamps and pointClouds
        self.truePointCloud = {}
        self.modeledPointCloud = {}

        self.imgWidth = 0
        self.imgHeight = 0


# Static class for reading in the data (TUM dataset format)
class DataReader:

    # Load in all data (according to the TUM dataset format)
    @staticmethod
    def loadTextFiles(path):
        dataObject = Data()
        dataObject.path = path
        # Get initial timestamps (will shrink due to the matching)
        timestamps = DataReader.getTimeStamps(os.path.join(path, "rgb.txt"))
        initialAmount = len(timestamps)

        # Get the first n datapoints (useful when dealing with huge dataset)
        if MAX_DATA_POINT_AMOUNT > 1:
            timestamps = timestamps[:MAX_DATA_POINT_AMOUNT]

        # Get, and match the filenames from the rgb and depth files
        dataObject.rgbFileNames, timestamps = DataReader.getFileNames(
            os.path.join(path, "rgb.txt"), timestamps)
        dataObject.depthFileNames, timestamps = DataReader.getFileNames(
            os.path.join(path, "depth.txt"), timestamps)

        # Get, and match the groundTruth
        dataObject.trueCamLocs, timestamps = DataReader().getTrueCameraLocations(
            os.path.join(path, "groundtruth.txt"), timestamps)

        # Get the final amount of stamps
        dataObject.timestamps = timestamps
        print("From", initialAmount, "there are", len(timestamps), "timestamps remaining! (Max datapoint amount parameter is",
              MAX_DATA_POINT_AMOUNT, ")")

        return dataObject

    # Have to match the timestamps from the different images manually
    # The Kinect from the dataset asynchronously returns RGB and depth images
    @staticmethod
    def matchTimeStamps(timestamps, matchDict):
        matches = associate(timestamps, matchDict)
        returnDict = dict([(timestamp, matchDict[matchKey])
                          for timestamp, matchKey in matches])

        return returnDict, list(returnDict.keys())

    # Get all the timestamps
    @staticmethod
    def getTimeStamps(path):
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]

        timestamps = [float(line.split(' ')[0]) for line in lines]
        timestamps.sort()  # We want to traverse the images in order

        return timestamps

    # Get all the image filenames from the timestamps
    @staticmethod
    def getFileNames(path, timestamps):
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]

        splitLines = [(float(line.split(' ')[0]), line.split(' ')[1])
                      for line in lines]

        return DataReader().matchTimeStamps(timestamps, dict(splitLines))

    # Get the ground truth according to the actual sensor data from the TUM dataset
    @staticmethod
    def getTrueCameraLocations(path, rgbDict):
        with open(path) as file:
            splitLines = [line.strip().split(' ')
                          for line in file if not line.startswith("#")]

        trueCamLocations = [(float(line[0]), CameraLocations().createFromText(line[1:]))
                            for line in splitLines]

        return DataReader().matchTimeStamps(rgbDict, dict(trueCamLocations))

    # Get the rgb and depth images, note that the rgb is 24 (8-8-8) bits, whilst depth is 16bit
    @staticmethod
    def getImagePair(dataObject, currTimeStamp):
        RGBFileName = dataObject.rgbFileNames[currTimeStamp]
        depthFileName = dataObject.depthFileNames[currTimeStamp]

        rgbImage = np.array(Image.open(os.path.join(
            dataObject.path, RGBFileName)), dtype=np.uint8)
        depthImage = np.array(Image.open(os.path.join(
            dataObject.path, depthFileName)), dtype=np.uint16)

        dataObject.imgWidth, dataObject.imgHeight = depthImage.shape

        return rgbImage, depthImage
