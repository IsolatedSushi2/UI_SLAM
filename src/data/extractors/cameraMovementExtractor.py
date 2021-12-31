import cv2
import numpy as np
from src.data.dataReader import CameraLocations
from pyquaternion import Quaternion

class CameraMovementExtractor:
    @staticmethod
    def extractCameraMovement(data):
        print("LL",len(data.timestamps))
        
        firstTimeStamp = data.timestamps[0]
        firstLoc = data.trueCamLocs[firstTimeStamp]
        data.modeledCamLocs[firstTimeStamp] = CameraLocations().createFromValues(firstLoc.translation, firstLoc.quaternion)

        for index, timeStamp in enumerate(data.timestamps[:-1]):
            nextTimestep = data.timestamps[index+ 1]
            trueNextLocation = data.trueCamLocs[nextTimestep]
            
            stereoFrame = data.stereoFrames[timeStamp]
            E = stereoFrame.getEssentialMatrix()
            points, R, t, mask = CameraMovementExtractor.getCameraMovementEssentialMatrix(stereoFrame)

            rotationQuaternion = Quaternion(matrix=(R))
            finalQuaternion = rotationQuaternion * data.modeledCamLocs[timeStamp].quaternion
            #np.array([float(translation[0]), float(translation[1]), float(translation[2])])
            
            data.modeledCamLocs[nextTimestep] = CameraLocations().createFromValues(trueNextLocation.translation, finalQuaternion)
        return data




    # This doesn't work very well, also still need to get the scaled translation vector
    @staticmethod
    def getCameraMovementEssentialMatrix(stereoFrame):
        pts_l_norm = cv2.undistortPoints(np.expand_dims(stereoFrame.pts1, axis=1), cameraMatrix=stereoFrame.K, distCoeffs=None)
        pts_r_norm = cv2.undistortPoints(np.expand_dims(stereoFrame.pts2, axis=1), cameraMatrix=stereoFrame.K, distCoeffs=None)


        points1 = pts_l_norm
        points2 = pts_r_norm

        # points1 = stereoFrame.pts1
        # points2 = stereoFrame.pts2

        # E, mask = cv2.findEssentialMat(pts_l_norm, pts_r_norm, focal=1.0, pp=(0., 0.), method=cv2.RANSAC, prob=0.999, threshold=3.0)
        camParams = stereoFrame.frame1.camParams
        E, mask = cv2.findEssentialMat(points1, points2, focal=1.0, pp=(0., 0.), method=cv2.RANSAC, prob=0.999, threshold=1.0)
        return cv2.recoverPose(E, points1, points2, focal=1.0, pp=(0., 0.))

        return cv2.recoverPose(E, points1, points2)
        #return cv2.recoverPose(E, pts_l_norm, pts_r_norm)