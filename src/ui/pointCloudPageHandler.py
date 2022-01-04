import numpy as np
from vispy import scene
from vispy.scene import visuals
from PyQt5.QtCore import QTimer
import gc
from pyquaternion import Quaternion
from src.constants import MAX_POINTS_PER_CLOUD_RATIO, POINT_CLOUD_PAGE_INDEX


# Handles the pointcloud page
class PointCloudPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.allTruePos = np.empty((0, 3))
        self.allTrueColors = np.empty((0, 3))

        self.setupWidget()
        self.addSceneVisuals()

        self.truePositions, self.trueColours = self.getRenders(
            self.data.truePointCloud.values())
        self.renderPoints()

    # Create the 3d vispy widget
    def setupWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor=(28/255, 31/255, 36/255), vsync=False)
        self.ui.pointCloudPage.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.view.camera = 'turntable'  # or try 'arcball'

    def addSceneVisuals(self):
        # For the points
        self.scatter = visuals.Markers()

        self.scatter.set_gl_state('opaque', depth_test=False)
        self.scatter.set_data(pos=np.random.normal(size=(
            1, 3), scale=0.2), edge_color=None, face_color=(1, 1, 1, .5), size=10, scaling=True)

        self.view.add(self.scatter)

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)

    # Get the indiced renders
    def getRenders(self, pointClouds):
        truePos, trueColors = zip(*pointClouds)

        return np.concatenate(truePos[self.ui.start: self.ui.end]), np.concatenate(trueColors[self.ui.start: self.ui.end])

    # Render the pointclouds
    def renderPoints(self):
        self.scatter.set_data(pos=self.truePositions, edge_width=0,
                              face_color=self.trueColours, size=1, scaling=False)

    def setSceneVisualsData(self, newSelect=False):
        self.truePositions, self.trueColours = self.getRenders(
            self.data.truePointCloud.values())
        self.renderPoints()
