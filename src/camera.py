import numpy as np


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


class Camera:
    def __init__(self):
        self.position = np.float64([0, 0, 0])
        self.rotation = np.identity(3)
        self.color = [0, 0, 0]

        self.radius = 0.1
        self.height = 0.15
        self.resolution = 10
        self.split = 3

    def moveCamera(self, translation, rotation):
        self.rotation = np.dot(rotation, self.rotation)
        self.position = self.position + np.dot(1 * self.rotation, translation)
        return self

    def getRenderedCamera(self, last):
        raise NotImplementedError()
