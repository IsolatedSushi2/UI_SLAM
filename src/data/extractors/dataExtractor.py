from src.data.dataReader import DataReader
from src.data.extractors.pointCloudExtractor import PointCloudExtractor
from src.data.extractors.imageExtractor import ImageExtractor
from src.constants import POINTCLOUD_INCREMENT_AMOUNT, MAX_POINTS_PER_CLOUD_RATIO
from src.slamAlgorithms.exampleSLAM import ExampleSLAM

import time


class DataExtractor:

    @staticmethod
    def loadDirectory(path, camParams):
        data = DataReader.loadTextFiles(path)

        data = DataExtractor.extractFrames(data, camParams)
        print("Extracted all Frames")
        data = DataExtractor.getStereoFrames(data)
        print("Extracted all StereoFrames")
        SLAMAlgorithm = ExampleSLAM(data)
        data = SLAMAlgorithm.extractCameraMovement()
        return data

    @staticmethod
    def getStereoFrames(data):
        for index in range(len(data.frames) - 1):
            currTimeStamp = data.timestamps[index]
            nextTimeStamp = data.timestamps[index + 1]

            currFrame = data.frames[currTimeStamp]
            nextFrame = data.frames[nextTimeStamp]

            stereoFrame = ImageExtractor.getStereoFrame(currFrame, nextFrame)
            data.stereoFrames[currTimeStamp] = stereoFrame

        return data

    @staticmethod
    def extractFrames(data, camParams):
        # Get the frames and pointClouds
        for index, timestamp in enumerate(data.timestamps):
            # Check whether to store the pointCloud
            renderPointCloud = index % POINTCLOUD_INCREMENT_AMOUNT == 0

            frame, pointCloud = DataExtractor.extractFrameAndPC(
                data, timestamp, camParams, renderPointCloud)
            data.frames[timestamp] = frame

            if pointCloud:
                data.truePointCloud[timestamp] = pointCloud
        return data

    @staticmethod
    def extractFrameAndPC(data, timestamp, camParams, renderPointCloud):
        (currRGBImage, currDepthImage) = DataReader.getImagePair(data, timestamp)
        frame = ImageExtractor.getFrame(
            timestamp, currRGBImage, currDepthImage, camParams)

        indices = frame.getRoundedKeypointIndices()
        points, _, depthmask = PointCloudExtractor.generate_point_cloud_improved(
            currRGBImage, currDepthImage, indices, camParams)

        frame.relativeKPSPointCloud = points
        print(len(frame.relativeKPSPointCloud))
        cameraLoc = data.trueCamLocs[timestamp]
        pointCloud = None
        if renderPointCloud:
            indices = PointCloudExtractor.getSamplePointsIndices(
                data.imgWidth, data.imgHeight, MAX_POINTS_PER_CLOUD_RATIO)
            points, colors, _ = PointCloudExtractor.generate_point_cloud_improved(
                currRGBImage, currDepthImage, indices, camParams)
            pointCloud = PointCloudExtractor.translate_point_cloud(
                points, colors, cameraLoc)

        return frame, pointCloud
