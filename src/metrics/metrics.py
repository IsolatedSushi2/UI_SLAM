import numpy as np


class Metrics:

    @staticmethod
    def getPosErrorPerStep(data, timestamps):

        allDistances = []

        for index, timestamp in enumerate(timestamps):

            modeledPos = data.modeledCamLocs[timestamp].translation
            truePos = data.trueCamLocs[timestamp].translation

            distance = np.linalg.norm(modeledPos - truePos)
            allDistances.append((index, distance))

        return np.array(allDistances)

    @staticmethod
    def getKeyMatchAmountPerStep(data, timestamps):

        keypointAmounts = []

        for index, timestamp in enumerate(timestamps):
            
            currFrame = data.frames[timestamp]
            keypointAmount = len(currFrame.keypoints)
            keypointAmounts.append((index, keypointAmount))

        return np.array(keypointAmounts)

    @staticmethod
    def getRotationErrorPerStep(data, timestamps):

        allRotErrors = []

        for index, timestamp in enumerate(timestamps):
            
            modeledQuat = data.modeledCamLocs[timestamp].quaternion
            trueQuat = data.trueCamLocs[timestamp].quaternion


            Aflat = modeledQuat.rotation_matrix.reshape(-1)  # views
            Bflat = trueQuat.rotation_matrix.reshape(-1)

            dotProduct = np.dot(Aflat, Bflat)
            scaling = max(np.linalg.norm(Aflat) * np.linalg.norm(Bflat), 1e-10)

            allignment = dotProduct / scaling
            # Error is difference to 1
            allRotErrors.append((index, abs(1 - allignment)))

        return np.array(allRotErrors)

    @staticmethod
    def getVelocityPerStep(data, timestamps):

        trueVelocities = []
        modeledVelocities = []

        for index in range(len(timestamps) - 1):
            currTimestamp = timestamps[index]
            nextTimestamp = timestamps[index + 1]
            
            currmodeledPos = data.modeledCamLocs[currTimestamp].translation
            currtruePos = data.trueCamLocs[currTimestamp].translation

            lastModeledPos = data.modeledCamLocs[nextTimestamp].translation
            lastTruePos = data.trueCamLocs[nextTimestamp].translation

            modeledDistance = np.linalg.norm(currmodeledPos - lastModeledPos)
            trueDistance = np.linalg.norm(currmodeledPos - lastTruePos)

            modeledVelocities.append((index, modeledDistance))
            trueVelocities.append((index, trueDistance))

        return np.array(modeledVelocities), np.array(trueVelocities)