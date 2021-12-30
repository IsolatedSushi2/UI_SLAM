#import warnings
#warnings.filterwarnings("ignore")

import os
import numpy as np
import cv2
from PIL import Image
from src.constants import MAX_DATA_POINT_AMOUNT, DATA_INCREMENT_AMOUNT
from src.associate import read_file_list, associate


class GroundTruthRow:
    def __init__(self, data):
        
        # Test whether correct data has been passed
        assert len(data) == 7

        self.translation = np.array([float(data[0]), float(data[1]), float(data[2])])
        self.quaternion = np.array([float(data[3]), float(data[4]), float(data[5]), float(data[6])])


class Data:
    def __init__(self):
        # List containing timestamps
        self.timestamps = []

        # Dictionaries containing the timestamps and fileNames
        self.rgbFileNames = {}
        self.depthFileNames = {}

        # Dictionaries containing the timestamps and ground truth movement relative to origin
        self.groundTruth = {}

        # Dictionaries containing the timestamps and the image
        self.rgbImages = {}
        self.depthImages = {}


class DataReader:

    # Load in all data (according to the TUM dataset format)
    @staticmethod 
    def loadDirectory(path):
        dataObject = Data()
        # Get initial timestamps (will shrink due to the matching)
        timestamps = DataReader.getTimeStamps(os.path.join(path, "rgb.txt"))
        initialAmount = len(timestamps)

        # Get the first n datapoints (useful when dealing with huge dataset)
        if MAX_DATA_POINT_AMOUNT > 1:
            timestamps = timestamps[:MAX_DATA_POINT_AMOUNT]
        
        # Get, and match the filenames from the rgb and depth files
        dataObject.rgbFileNames, timestamps = DataReader.getFileNames(os.path.join(path, "rgb.txt"), timestamps)
        dataObject.depthFileNames, timestamps = DataReader.getFileNames(os.path.join(path, "depth.txt"), timestamps)

        # Get, and match the groundTruth
        dataObject.groundTruth, timestamps = DataReader().getGroundTruth(os.path.join(path, "groundtruth.txt"), timestamps)

        timestamps = timestamps[::DATA_INCREMENT_AMOUNT]

        # Get the images from the matched timestamps
        dataObject.rgbImages = DataReader().getImages(path, timestamps, dataObject.rgbFileNames, np.uint8)
        dataObject.depthImages = DataReader().getImages(path, timestamps, dataObject.depthFileNames, np.uint16)

        #Get the final amount of stamps
        dataObject.timestamps = timestamps
        print("From", initialAmount, "there are", len(timestamps), "timestamps remaining! (Max datapoint amount parameter is", MAX_DATA_POINT_AMOUNT, "and increment amount is", DATA_INCREMENT_AMOUNT, ")")

        return dataObject

    # Have to match the timestamps from the different images manually TODO fix when a match cannot be found
    @staticmethod
    def matchTimeStamps(timestamps, matchDict):
        matches = associate(timestamps, matchDict)       
        returnDict = dict([(timestamp, matchDict[matchKey]) for timestamp, matchKey in matches])

        # assert len(returnDict.keys()) == len(rgbDict.keys()), "Error with matching timestamps {} {}".format(len(returnDict.keys()), len(rgbDict.keys()))
        return returnDict, list(returnDict.keys())

    # Get all the timestamps
    @staticmethod
    def getTimeStamps(path):
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]

        timestamps = [float(line.split(' ')[0]) for line in lines]
        timestamps.sort()

        return timestamps
    
    # Get all the image filenames from the timestamps
    @staticmethod
    def getFileNames(path, timestamps):
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]

        splitLines = [(float(line.split(' ')[0]), line.split(' ')[1]) for line in lines]
        
        return DataReader().matchTimeStamps(timestamps, dict(splitLines))

    # Get the ground truth according to the actual sensor data from the TUM dataset
    @staticmethod
    def getGroundTruth(path, rgbDict):
        with open(path) as file:
            splitLines = [line.strip().split(' ') for line in file if not line.startswith("#")]
        
        groundTruths = [(float(line[0]), GroundTruthRow(line[1:])) for line in splitLines]
        
        return DataReader().matchTimeStamps(rgbDict, dict(groundTruths))

    # Get the rgb and depth images, note that the rgb is 24 (8-8-8) bits, whilst depth is 16bit
    @staticmethod
    def getImages(path, activeTimeStamps, fileNames, dtype):
        returnDict = {}

        for currTimeStamp in activeTimeStamps:
            currFileName = fileNames[currTimeStamp]
            currImage = np.array(Image.open(os.path.join(path, currFileName)), dtype=dtype)            
            returnDict[currTimeStamp] = currImage

        return returnDict