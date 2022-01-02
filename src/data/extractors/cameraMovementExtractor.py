import cv2
import numpy as np
from src.data.dataReader import CameraLocations
from src.data.extractors.pointCloudExtractor import PointCloudExtractor
from pyquaternion import Quaternion


class CameraMovementExtractor:
    @staticmethod
    def extractCameraMovement(data):
        print("There are", len(data.timestamps), "timestamps")

        # Get the initial translation and rotation
        firstTimeStamp = data.timestamps[0]
        firstLoc = data.trueCamLocs[firstTimeStamp]
        data.modeledCamLocs[firstTimeStamp] = CameraLocations(
        ).createFromValues(firstLoc.translation, firstLoc.quaternion)

        for index, timeStamp in enumerate(data.timestamps[:-1]):
            nextTimeStamp = data.timestamps[index + 1]
            
            # Debugging purposes
            trueCurrLocation = data.trueCamLocs[timeStamp]
            trueNextLocation = data.trueCamLocs[nextTimeStamp]

            modeledLocation = data.modeledCamLocs[timeStamp]

            stereoFrame = data.stereoFrames[timeStamp]

            # Get the 3dPositions of the first frame            
            firstFrameIndices = stereoFrame.getMatchesIndices(1)
            framePoints = np.array([stereoFrame.frame1.relativeKPSPointCloud[tuple(currFrame)] for currFrame in firstFrameIndices])
            
            #positions3D, _ = PointCloudExtractor.translate_point_cloud(framePoints, None, modeledLocation)
            positions3D, _ = PointCloudExtractor.translate_point_cloud(framePoints, None, trueCurrLocation)

            succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(positions3D, stereoFrame.pts2, stereoFrame.K, None)
            rotationMatrix, _ = cv2.Rodrigues(rVector)

            cameraRotation = rotationMatrix.T
            cameraLocation = np.array(-np.matrix(cameraRotation) * np.matrix(rTrans))
            
            cameraLocation = np.array([float(cameraLocation[0]), float(cameraLocation[1]), float(cameraLocation[2])])

            
            if not succes:
                print("SOLVEPNP ERROR")
            #finalQuaternion = Quaternion(matrix=cameraLocation)
            
            # print("Succes", succes)

            # print(trueNextLocation.translation, "Real Location")
            
            # print("Calculated Rotation:\n", cameraRotation)
            # print("Real Rotation:\n", trueNextLocation.quaternion.rotation_matrix)

            finalQuaternion = Quaternion(matrix=cameraRotation)

            data.modeledCamLocs[nextTimeStamp] = CameraLocations().createFromValues(
                cameraLocation, finalQuaternion)
        return data

    @staticmethod
    def debugCamera2(data):
        firstTimeStamp = data.timestamps[0]
        firstLoc = data.trueCamLocs[firstTimeStamp]

        stereoFrame = data.stereoFrames[firstTimeStamp]

        firstFrameIndices = stereoFrame.frame1.realKPS

        firstFramePoints = np.array([stereoFrame.frame1.relativeKPSPointCloud[tuple(currFrame)] for currFrame in firstFrameIndices])
        firstPositions3D, _ = PointCloudExtractor.translate_point_cloud(firstFramePoints, None, firstLoc)
        succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(firstPositions3D, stereoFrame.frame1.realKPS, stereoFrame.K, None)

        rotationMatrix, _ = cv2.Rodrigues(rVector)

        cameraRotation = rotationMatrix.T
        cameraLocation = (-np.matrix(cameraRotation) * np.matrix(rTrans)).reshape((3,))

        print("Succes", succes)
        print(cameraLocation.flatten(), "Calculated Camera Location", )
        print(firstLoc.translation, "Real Location")
        
        print("Calculated Rotation:\n", cameraRotation)
        print("Real Rotation:\n", firstLoc.quaternion.rotation_matrix)
        

    @staticmethod
    def debugCamera(data):
        firstTimeStamp = data.timestamps[0]
        firstLoc = data.trueCamLocs[firstTimeStamp]

        secondTimeStamp = data.timestamps[1]
        secondLoc = data.trueCamLocs[secondTimeStamp]

        stereoFrame = data.stereoFrames[firstTimeStamp]

        firstFrameIndices = stereoFrame.frame(1)
        secondFrameIndices = stereoFrame.getMatchesIndices(2)

        firstFramePoints = np.array([stereoFrame.frame1.relativeKPSPointCloud[tuple(currFrame)] for currFrame in firstFrameIndices])
        secondFramePoints = np.array([stereoFrame.frame2.relativeKPSPointCloud[tuple(currFrame)] for currFrame in secondFrameIndices])

        firstPositions3D, _ = PointCloudExtractor.translate_point_cloud(firstFramePoints, None, firstLoc)
        secibdPositions3D, _ = PointCloudExtractor.translate_point_cloud(secondFramePoints, None, secondLoc)

        succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(firstPositions3D, stereoFrame.pts1, stereoFrame.K, None)
        rTrans = rTrans.flatten()

        print("Succes", succes)
        print("realLoc", firstLoc.translation)
        print("-----------")
        print(rTrans)



    @staticmethod
    def getCameraMovementPNP(stereoFrame):
        return

    # This doesn't work very well, also still need to get the scaled translation vector
    @staticmethod
    def getCameraMovementEssentialMatrix(stereoFrame):
        pts_l_norm = cv2.undistortPoints(np.expand_dims(
            stereoFrame.pts1, axis=1), cameraMatrix=stereoFrame.K, distCoeffs=None)
        pts_r_norm = cv2.undistortPoints(np.expand_dims(
            stereoFrame.pts2, axis=1), cameraMatrix=stereoFrame.K, distCoeffs=None)

        points1 = pts_l_norm
        points2 = pts_r_norm

        # points1 = stereoFrame.pts1
        # points2 = stereoFrame.pts2

        # E, mask = cv2.findEssentialMat(pts_l_norm, pts_r_norm, focal=1.0, pp=(0., 0.), method=cv2.RANSAC, prob=0.999, threshold=3.0)
        camParams = stereoFrame.frame1.camParams
        E, mask = cv2.findEssentialMat(points1, points2, focal=1.0, pp=(
            0., 0.), method=cv2.RANSAC, prob=0.999, threshold=1.0)
        return cv2.recoverPose(E, points1, points2, focal=1.0, pp=(0., 0.))

        return cv2.recoverPose(E, points1, points2)
        # return cv2.recoverPose(E, pts_l_norm, pts_r_norm)
