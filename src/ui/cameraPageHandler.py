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

        self.createVispyWidget()
        self.addSceneVisuals()
        self.createRangeSliderWidget(len(self.data.timestamps))

        self.trueCameras, self.trueDirections = self.getRenders(self.data.trueCamLocs)
        self.modeledCameras, self.modeledDirections = self.getRenders(self.data.modeledCamLocs)


        self.ui.renderGroundTruthCheckBox.stateChanged.connect(self.setSceneVisualsData)
        self.ui.renderModeledCheckBox.stateChanged.connect(self.setSceneVisualsData)


        self.setSceneVisualsData()

    # Create the 3d vispy widget
    def createVispyWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor='black')
        self.ui.cameraRenderPlace.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.view.camera = 'turntable'  # scene.cameras.FlyCamera()  # or try 'arcball'

    # Create the range slider widget
    def createRangeSliderWidget(self, cameraAmount):
        self.rangeSlider = QRangeSlider()

        self.rangeSlider.setMaximumHeight(20)
        self.rangeSlider.setMax(cameraAmount)
        self.rangeSlider.setEnd(cameraAmount)

        # When value change, update
        self.rangeSlider.startValueChanged.connect(self.setSceneVisualsData)
        self.rangeSlider.endValueChanged.connect(self.setSceneVisualsData)

        self.ui.cameraRenderPlace.layout().addWidget(self.rangeSlider)

    # Get the camera location, including its translation and rotation
    def getRenders(self, cameraLocations):
        cameras = []
        lines = []

        # TODO THE INDEXING
        for timestamps in self.data.timestamps[:-1]:
            currCamera = cameraLocations[timestamps]

            # Use the forward vector (Unity mindset) to get a point which the camera is directed to
            rotated = currCamera.quaternion.rotate(np.array([0, 0, 0.04]))

            cameras.append(currCamera.translation)
            lines.append(currCamera.translation)
            lines.append(currCamera.translation + rotated)

        return np.array(cameras), np.array(lines)

    # To get a nice gradient
    def getColours(self, amount, col1, col2):
        red = Color(col1)
        colors = list(red.range_to(Color(col2), amount))

        return np.asarray([color.rgb for color in colors])

    def addSceneVisuals(self):
        # For the camera positions
        self.trueScatter = visuals.Markers()
        self.trueScatter.set_gl_state('translucent', depth_test=False)
        self.view.add(self.trueScatter)

        self.modeledScatter = visuals.Markers()
        self.modeledScatter.set_gl_state('translucent', depth_test=False)
        self.view.add(self.modeledScatter)

        # For the line positions
        self.trueLines = visuals.Line()
        self.view.add(self.trueLines)

        self.modeledLines = visuals.Line()
        self.view.add(self.modeledLines)

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)

    def clearScreen(self):
        emptyData = np.empty((0, 3))

        self.trueScatter.set_data(np.empty((0, 3)), face_color=(1, 1, 1, 1))
        self.modeledScatter.set_data(np.empty((0, 3)), face_color=(1, 1, 1, 1))

        self.trueLines.set_data(np.empty((0, 3)), color=(1, 1, 1, 1))
        self.modeledLines.set_data(np.empty((0, 3)), color=(1, 1, 1, 1))

    def getSlicedRenders(self, cams, directions, col1, col2):
        currCameras = cams[self.rangeSlider.start(): self.rangeSlider.end()]
        currDirections = directions[self.rangeSlider.start() * 2: self.rangeSlider.end() * 2]

        pointColors = self.getColours(len(currCameras), col1, col2)
        lineColors = np.repeat(pointColors, 2, axis=0)

        return currCameras, currDirections, pointColors, lineColors

    def renderTrueCameras(self):
        trueData = self.getSlicedRenders(self.trueCameras, self.trueDirections, 'yellow', 'green')
        currCams, currDirects, pointColors, lineColors = trueData
        print(currCams[0])
        print(currCams.shape)
        self.trueScatter.set_data(currCams, edge_color=None,
                                face_color=pointColors, size=10, scaling=False)
        self.trueLines.set_data(pos=currDirects, color=lineColors, connect="segments")

    def renderModeledCameras(self):
        modeledData = self.getSlicedRenders(self.modeledCameras, self.modeledDirections, 'blue', 'red')
        currCams, currDirects, pointColors, lineColors = modeledData
        print(currCams[0])
        print(currCams.shape)
        print(currCams[0].shape)
        self.modeledScatter.set_data(currCams, edge_color=None,
                                face_color=pointColors, size=10, scaling=False)
        self.modeledLines.set_data(pos=currDirects, color=lineColors, connect="segments")

    def setSceneVisualsData(self):
        # Slice the selected cameras according to the rangeslider

        self.clearScreen()

        if self.ui.renderGroundTruthCheckBox.isChecked():
            self.renderTrueCameras()
        
        if self.ui.renderModeledCheckBox.isChecked():
            self.renderModeledCameras()
            pass