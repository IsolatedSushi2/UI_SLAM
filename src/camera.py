import numpy as np


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