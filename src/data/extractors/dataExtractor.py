from src.data.dataReader import DataReader
from src.data.extractors.pointCloudExtractor import PointCloudExtractor
from src.data.extractors.imageExtractor import ImageExtractor
from src.constants import POINTCLOUD_INCREMENT_AMOUNT, MAX_POINTS_PER_CLOUD_RATIO
from src.data.extractors.cameraMovementExtractor import CameraMovementExtractor
import time
class DataExtractor:

    @staticmethod
    def loadDirectory(path, camParams):
        data = DataReader.loadTextFiles(path)
        print("Read in text")

        time1 = time.time()
        data = DataExtractor.extractData(data, camParams)
        print("Extracting stereoFrames", time.time() - time1)

        data = CameraMovementExtractor.extractCameraMovement(data)
        return data

    @staticmethod
    def extractData(data, camParams):

        # Get the frames and pointClouds
        for index, timestamp in enumerate(data.timestamps):
            renderPointCloud = index % POINTCLOUD_INCREMENT_AMOUNT == 0
            frame, pointCloud = DataExtractor.extractFrameAndPC(data, timestamp, camParams, renderPointCloud)
            data.frames[timestamp] = frame

            if renderPointCloud:
                data.truePointCloud[timestamp] = pointCloud

        print("Extracted all Frames")

        # Get the StereoFrames (stereoframe can be referenced by the timestamp of the first frame)
        for index in range(len(data.frames) - 1):
            timestamp1 = data.timestamps[index]
            timestamp2 = data.timestamps[index + 1]

            frame1 = data.frames[timestamp1]
            frame2 = data.frames[timestamp2]

            stereoFrame = ImageExtractor.getStereoFrame(frame1, frame2)
            data.stereoFrames[timestamp1] = stereoFrame
        

        print("Extracted all StereoFrames")

        return data

    @staticmethod
    def extractFrameAndPC(data, timestamp, camParams, renderPointCloud):
        (currRGBImage, currDepthImage) = DataReader.getImagePair(data, timestamp)
        frame = ImageExtractor.getFrame(timestamp, currRGBImage, currDepthImage, camParams)

        cameraLoc = data.trueCamLocs[timestamp]
        pointCloud = None

        if renderPointCloud:
            indices = PointCloudExtractor.getSamplePointsIndices(data.imgWidth, data.imgHeight, MAX_POINTS_PER_CLOUD_RATIO)
            points, colors = PointCloudExtractor.generate_point_cloud_improved(currRGBImage, currDepthImage, indices, camParams)
            pointCloud = PointCloudExtractor.translate_point_cloud(points, colors, cameraLoc)
            #pointCloud = PointCloudExtractor.generate_point_cloud_improved(currRGBImage, currDepthImage, cameraLoc, camParams)

        return frame, pointCloud