#import warnings
#warnings.filterwarnings("ignore")

import os
import numpy as np
import cv2
from PIL import Image

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

    @staticmethod
    def loadDirectory(path):
        dataObject = Data()

        dataObject.timestamps = DataReader.getTimeStamps(os.path.join(path, "rgb.txt"))
        dataObject.rgbFileNames = DataReader.getFileNames(os.path.join(path, "rgb.txt"))
        dataObject.groundTruth = DataReader().getGroundTruth(os.path.join(path, "groundtruth.txt"), dataObject.rgbFileNames)
        dataObject.depthFileNames = DataReader.getFileNames(os.path.join(path, "depth.txt"), dataObject.rgbFileNames)
        dataObject.rgbImages = DataReader().getImages(path, dataObject.timestamps, dataObject.rgbFileNames)
        dataObject.depthImages = DataReader().getImages(path, dataObject.timestamps, dataObject.depthFileNames, True)

        return dataObject

    @staticmethod
    def matchTimeStamps(rgbDict, matchDict):
        matches = associate(rgbDict, matchDict)       
        returnDict = dict([(rgbKey, matchDict[matchKey]) for rgbKey, matchKey in matches])

        assert len(returnDict.keys()) == len(rgbDict.keys()), "Error with matching timestamps"
        return returnDict



    @staticmethod
    def getTimeStamps(path):
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]

        timestamps = [float(line.split(' ')[0]) for line in lines]
        timestamps.sort()

        return timestamps
    
    @staticmethod
    def getFileNames(path, rgbDict = None):
        with open(path) as file:
            lines = [line.strip() for line in file if not line.startswith("#")]

        splitLines = [(float(line.split(' ')[0]), line.split(' ')[1]) for line in lines]
        
        if rgbDict:
            return DataReader().matchTimeStamps(rgbDict, dict(splitLines))

        return dict(splitLines)

    @staticmethod
    def getGroundTruth(path, rgbDict):
        with open(path) as file:
            splitLines = [line.strip().split(' ') for line in file if not line.startswith("#")]
        
        groundTruths = [(float(line[0]), GroundTruthRow(line[1:])) for line in splitLines]
        
        return DataReader().matchTimeStamps(rgbDict, dict(groundTruths))

    @staticmethod
    def getImages(path, activeTimeStamps, fileNames, depth=False):
        returnDict = {}

        for currTimeStamp in activeTimeStamps:
            currFileName = fileNames[currTimeStamp]
            currImage = np.array(Image.open(os.path.join(path, currFileName)))

            
            returnDict[currTimeStamp] = currImage

        return returnDict