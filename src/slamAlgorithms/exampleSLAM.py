from src.slamAlgorithms.baseSLAM import BaseSLAM
import cv2
import numpy as np
from src.camera import CameraLocations
from src.data.extractors.pointCloudExtractor import PointCloudExtractor
from pyquaternion import Quaternion
#  Simple SLAM algorithm (one relative constraint per stereoFrame)


class ExampleSLAM(BaseSLAM):
    def __init__(self, data):
        self.data = data

    def extractCameraMovement(self):

        # Get the initial translation and rotation
        firstTimeStamp = self.data.timestamps[0]
        firstLoc = self.data.trueCamLocs[firstTimeStamp]
        self.data.modeledCamLocs[firstTimeStamp] = CameraLocations(
        ).createFromValues(firstLoc.translation, firstLoc.quaternion)

        self.data = self.calculateCameraLocations()
        self.printAllResults(10)

        return self.data

    def calculateCameraLocations(self):
        for index, timeStamp in enumerate(self.data.timestamps[:-1]):
            nextTimeStamp = self.data.timestamps[index + 1]

            # Debugging purposes
            trueCurrLocation = self.data.trueCamLocs[timeStamp]
            trueNextLocation = self.data.trueCamLocs[nextTimeStamp]

            modeledLocation = self.data.modeledCamLocs[timeStamp]

            stereoFrame = self.data.stereoFrames[timeStamp]

            relativePositions3D = stereoFrame.frame1KPS

            positions3D, _ = PointCloudExtractor.translate_point_cloud(
                relativePositions3D, None, trueCurrLocation)
            # positions3D, _ = PointCloudExtractor.translate_point_cloud(
            #     relativePositions3D, None, modeledLocation)

            cameraLoc = self.getCameraLocationPNP(positions3D, stereoFrame.pts2, stereoFrame.K)
            self.data.modeledCamLocs[nextTimeStamp] = cameraLoc

        return self.data

    def printAllResults(self, amount):
        for timestamp in self.data.timestamps[:amount]:
            self.printResults(timestamp)

    # Debugging purposes
    def printResults(self, timestamp):
        trueLoc = self.data.trueCamLocs[timestamp]
        modeledLoc = self.data.modeledCamLocs[timestamp]
        print("True: Modeled:")
        print(trueLoc.translation, modeledLoc.translation)

    def getCameraLocationPNP(self, points3D, points2D, cameraMatrix):
        succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(
            points3D, points2D, cameraMatrix, None)

        assert succes is True

        # Get the camera position and location in world space
        cameraRotation = cv2.Rodrigues(rVector)[0].T
        cameraTranslation = np.array(-np.matrix(cameraRotation) * np.matrix(rTrans))

        # TODO, simplify this
        cameraTranslation = np.array([float(cameraTranslation[0]), float(
            cameraTranslation[1]), float(cameraTranslation[2])])

        finalQuaternion = Quaternion(matrix=cameraRotation)
        return CameraLocations().createFromValues(cameraTranslation, finalQuaternion)
