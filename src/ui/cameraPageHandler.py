import numpy as np
from vispy import scene
from vispy.scene import visuals
from colour import Color
from pyquaternion import Quaternion
from src.ui.rangeslider import QRangeSlider
from PyQt5 import QtCore, QtGui, QtWidgets


class CameraPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0

        self.createVispyWidget()

        self.addSceneVisuals()

        self.cameras, self.directions = self.getRenders()
        self.createRangeSliderWidget()

        self.setSceneVisualsData()

    # Create the 3d vispy widget
    def createVispyWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor='black')
        self.ui.camera3dPage.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.view.camera = 'turntable'  # scene.cameras.FlyCamera()  # or try 'arcball'

    # Create the range slider widget
    def createRangeSliderWidget(self):
        self.rangeSlider = QRangeSlider()

        self.rangeSlider.setMaximumHeight(20)
        self.rangeSlider.setMax(len(self.cameras))
        self.rangeSlider.setEnd(len(self.cameras))

        # When value change, update
        self.rangeSlider.startValueChanged.connect(self.setSceneVisualsData)
        self.rangeSlider.endValueChanged.connect(self.setSceneVisualsData)

        self.ui.camera3dPage.layout().addWidget(self.rangeSlider)

    # Get the camera location, including its translation and rotation
    def getRenders(self):
        cameras = []
        lines = []

        for timestamps in self.data.groundTruth.keys():
            currGroundTruth = self.data.groundTruth[timestamps]

            # Get the cameras location / rotation
            x, y, z, w = tuple(currGroundTruth.quaternion)
            quaternion = Quaternion(w=w, x=x, y=y, z=z)

            # Use the forward vector (Unity mindset) to get a point which the camera is directed to
            rotated = quaternion.rotate(np.array([0, 0, 0.04]))

            cameras.append(currGroundTruth.translation)
            lines.append(currGroundTruth.translation)
            lines.append(rotated + currGroundTruth.translation)

        return np.array(cameras), np.array(lines)

    # To get a nice gradient
    def getColours(self, amount):
        red = Color("blue")
        colors = list(red.range_to(Color("red"), amount))

        return np.asarray([color.rgb for color in colors])

    def addSceneVisuals(self):
        # For the camera positions
        self.scatter = visuals.Markers()
        # TODO, find wtf this does exactly (something is getting messed up when using anti aliasing)
        self.scatter.set_gl_state('translucent', depth_test=False)
        self.view.add(self.scatter)

        # For the line positions
        self.lines = visuals.Line()
        self.view.add(self.lines)

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)

    def setSceneVisualsData(self):
        # Slice the selected cameras according to the rangeslider
        currCameras = self.cameras[self.rangeSlider.start(
        ): self.rangeSlider.end()]
        currDirections = self.directions[self.rangeSlider.start(
        ) * 2: self.rangeSlider.end() * 2]

        self.colors = self.getColours(len(currCameras))

        self.scatter.set_data(currCameras, edge_color=None,
                              face_color=self.colors, size=10, scaling=False)
        self.lines.set_data(pos=currDirections, color=np.repeat(
            self.colors, 2, axis=0), connect="segments")
