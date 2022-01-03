from src.slamAlgorithms.baseSLAM import BaseSLAM
import cv2
import numpy as np
from src.camera import CameraLocations
from src.data.extractors.pointCloudExtractor import PointCloudExtractor
from pyquaternion import Quaternion
#  Simple SLAM algorithm (one relative constraint per stereoFrame)
#  For now it uses the camera's true position in orde to find the location one frame ahead
#  Note that it is a very simple example! More complicated algorithms are required for better results
#  This project was about the framework instead of the development of state of the arts algorithms


class ExampleSLAM(BaseSLAM):
    def __init__(self, data):
        self.data = data

    def extractCameraMovement(self):

        # Get the initial translation and rotation
        firstTimeStamp = self.data.timestamps[0]
        firstLoc = self.data.trueCamLocs[firstTimeStamp]
        self.data.modeledCamLocs[firstTimeStamp] = CameraLocations(
        ).createFromValues(firstLoc.translation, firstLoc.quaternion)

        # Calculate locations
        self.data = self.calculateCameraLocations()

        return self.data

    def calculateCameraLocations(self):
        for index, timeStamp in enumerate(self.data.timestamps[:-1]):
            nextTimeStamp = self.data.timestamps[index + 1]

            # Debugging purposes
            trueCurrLocation = self.data.trueCamLocs[timeStamp]
            trueNextLocation = self.data.trueCamLocs[nextTimeStamp]

            modeledLocation = self.data.modeledCamLocs[timeStamp]

            stereoFrame = self.data.stereoFrames[timeStamp]

            # Calculate real positions in world space
            relativePositions3D = stereoFrame.frame1KPS
            positions3D, _ = PointCloudExtractor.translate_point_cloud(
                relativePositions3D, None, trueCurrLocation)

            # Find the cameras position
            cameraLoc = self.getCameraLocationPNP(
                positions3D, stereoFrame.pts2, stereoFrame.K)
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

        if len(points3D) <= 10:
            return None

        succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(
            points3D, points2D, cameraMatrix, None, confidence=0.999)

        if not succes:
            return None

        # Get the camera position and location in world space
        cameraRotation = cv2.Rodrigues(rVector)[0].T
        cameraTranslation = np.array(-np.matrix(cameraRotation)
                                     * np.matrix(rTrans))

        # TODO, simplify this (for some reason dtype=float didnt work)
        cameraTranslation = np.array([float(cameraTranslation[0]), float(
            cameraTranslation[1]), float(cameraTranslation[2])])

        finalQuaternion = Quaternion(matrix=cameraRotation)
        return CameraLocations().createFromValues(cameraTranslation, finalQuaternion)
