from src.slamAlgorithms.baseSLAM import BaseSLAM

#  Simple SLAM algorithm (one relative constraint per stereoFrame)


class ExampleSLAM(BaseSLAM):
    def __init__(self, data):
        self.data = data

    def extractCameraMovement():

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
            framePoints = np.array([stereoFrame.frame1.relativeKPSPointCloud[tuple(
                currFrame)] for currFrame in firstFrameIndices])

            #positions3D, _ = PointCloudExtractor.translate_point_cloud(framePoints, None, modeledLocation)
            positions3D, _ = PointCloudExtractor.translate_point_cloud(
                framePoints, None, trueCurrLocation)

            succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(
                positions3D, stereoFrame.pts2, stereoFrame.K, None)
            rotationMatrix, _ = cv2.Rodrigues(rVector)

            cameraRotation = rotationMatrix.T
            cameraLocation = np.array(-np.matrix(cameraRotation)
                                      * np.matrix(rTrans))

            cameraLocation = np.array([float(cameraLocation[0]), float(
                cameraLocation[1]), float(cameraLocation[2])])

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

    def getCameraLocationPNP(points3D, points2D, cameraMatrix):
        succes, rVector, rTrans, inLiers = cv2.solvePnPRansac(
            points3D, points2D, cameraMatrix, None)

        assert succes is True

        # Get the camera position and location in world space
        cameraRotation = cv2.Rodrigues(rVector).T
        cameraTranslation = np.array(-np.matrix(cameraRotation) * np.matrix(rTrans))

        # TODO, simplify this
        cameraTranslation = np.array([float(cameraLocation[0]), float(
            cameraLocation[1]), float(cameraLocation[2])])

        finalQuaternion = Quaternion(matrix=cameraRotation)
        return CameraLocations().createFromValues(cameraTranslation, finalQuaternion)
