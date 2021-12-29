import numpy as np
from vispy import scene
from vispy.scene import visuals
from PyQt5.QtCore import QTimer
import gc
from pyquaternion import Quaternion
from src.constants import MAX_POINTS_PER_CLOUD_RATIO, POINT_CLOUD_PAGE_INDEX

class PointCloudPageHandler:
    def __init__(self, ui, dataObject, cameraParameters):
        self.ui = ui
        self.data = dataObject
        self.camParams = cameraParameters

        self.allPos = np.empty((0,3))
        self.allColors = np.empty((0,3))

        self.currentFrameIndex = 0

        self.setupWidget()
        self.addSceneVisuals()
        
        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(10)

    # Create the 3d vispy widget
    def setupWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor='black', vsync=False)
        self.ui.pointCloudPage.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.view.camera = 'turntable'  # or try 'arcball'

    def addSceneVisuals(self):
        # For the points
        self.scatter = visuals.Markers()

        self.scatter.set_gl_state('opaque', depth_test=False)
        self.scatter.set_data(pos=np.random.normal(size=(1, 3), scale=0.2), edge_color=None, face_color=(1, 1, 1, .5), size=10, scaling=True)

        self.view.add(self.scatter)

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)

    # Inspired from the given generate_pointcloud.py, but optimised because it was way too slow
    def generate_point_cloud(self, timestamp, rotationMatrix):
        print("Generating")

        rgb = self.data.rgbImages[timestamp]
        depth = self.data.depthImages[timestamp]

        depthMask = depth != 0        
        width, height = depth.shape
       
        colors = rgb[depthMask] / 255  # Need value between 0 and 1
        depth = depth[depthMask]

        # Optimized numpy implementation instead of the slow for loops from the datasets authors
        Z = depth / self.camParams.depthScalingFactor
        u = np.tile(np.arange(width), (height, 1)).T[depthMask]
        v = np.tile(np.arange(height), (width, 1))[depthMask]
        X = np.multiply(v - self.camParams.centerx, Z / self.camParams.focalx)
        Y = np.multiply(u - self.camParams.centery, Z / self.camParams.focaly)

        positions = np.column_stack((X, Y, Z))
        transformedPositions = rotationMatrix.dot(positions.T).T + self.data.groundTruth[timestamp].translation
        return transformedPositions, colors

    def samplePoints(self, positions, colors, sampleRatio):
        sampledPoints = int(len(positions) * sampleRatio)
        sampledIndices = np.random.choice(range(len(positions)), sampledPoints, replace=False)

        return positions[sampledIndices], colors[sampledIndices]

    def renderPoints(self, points, colors):
        # Add the points and colours
        self.allPos = np.concatenate((self.allPos, points))
        self.allColors = np.concatenate((self.allColors, colors))

        self.scatter.set_data(pos=self.allPos, edge_width=0, face_color=self.allColors, size=1, scaling=False)
        self.currentFrameIndex = (self.currentFrameIndex + 20)

    def checkIfFinished(self):
        if self.currentFrameIndex < len(self.data.timestamps):
            return

        print("Finished generating all the pointclouds")
        self.timer.stop()

    def updateFrame(self):

        # Disable when not using the page (less computation and avoids the vispy memory leak bug)
        if self.ui.mainStackedWidget.currentIndex() != POINT_CLOUD_PAGE_INDEX:
            return

        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]

        x, y, z, w = tuple(self.data.groundTruth[currTimestamp].quaternion)
        quaternion = Quaternion(x=x, y=y, z=z, w=w)
        pos, colors = self.generate_point_cloud(currTimestamp, quaternion.rotation_matrix)

        # To not get too many points, sample using the given ratio
        pos, colors = self.samplePoints(pos, colors, MAX_POINTS_PER_CLOUD_RATIO)
        self.renderPoints(pos, colors)

        self.canvas.measure_fps()
        self.checkIfFinished()


        




