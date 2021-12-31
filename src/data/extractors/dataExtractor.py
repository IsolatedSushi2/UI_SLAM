from src.data.dataReader import DataReader
from src.data.extractors.pointCloudExtractor import PointCloudExtractor
from src.data.extractors.imageExtractor import ImageExtractor
from src.constants import POINTCLOUD_INCREMENT_AMOUNT
from src.data.extractors.cameraMovementExtractor import CameraMovementExtractor

class DataExtractor:

    @staticmethod
    def loadDirectory(path, camParams):
        data = DataReader.loadTextFiles(path)
        print("Readed in text")
        data = DataExtractor.extractData(data, camParams)
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
            pointCloud = PointCloudExtractor.generate_point_cloud(currRGBImage, currDepthImage, cameraLoc, camParams)

        return frame, pointCloud

