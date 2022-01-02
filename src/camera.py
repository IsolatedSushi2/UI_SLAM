import numpy as np
from pyquaternion import Quaternion

# Store the intrinsic parameters of the camera
class CameraParameters:
    def __init__(self, width, height, focalx, focaly, centerx, centery, depthScalingFactor):
        self.focalx = focalx
        self.focaly = focaly
        self.centerx = centerx
        self.centery = centery
        self.width = width
        self.height = height
        self.depthScalingFactor = depthScalingFactor

        self.K = self.getKMatrix()
        print("Camera Matrix:\n", self.K)

    def getKMatrix(self):
        return np.asmatrix([[self.focalx, 0, self.centerx],
                            [0, self.focaly, self.centery],
                            [0, 0, 1]])


class CameraLocations:
    def __init__(self):
        self.translation = None
        self.quaternion = None

    def createFromValues(self, translation, quaternion):
        self.translation = translation
        self.quaternion = quaternion

        return self

    def createFromText(self, data):
        # Test whether correct data has been passed
        assert len(data) == 7

        self.translation = np.array(
            [float(data[0]), float(data[1]), float(data[2])])
        self.quaternion = Quaternion(x=float(data[3]), y=float(
            data[4]), z=float(data[5]), w=float(data[6]))

        return self
