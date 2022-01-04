import numpy as np
from vispy import scene
from vispy.scene import visuals
from colour import Color
from pyquaternion import Quaternion
from PyQt5 import QtCore, QtGui, QtWidgets
from vispy.visuals.transforms import STTransform


# Handles the rendering of the camera positions
class CameraPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.createVispyWidget()
        self.addSceneVisuals()

        self.trueCameras, self.trueDirections = self.getRenders(
            self.data.trueCamLocs)
        self.modeledCameras, self.modeledDirections = self.getRenders(
            self.data.modeledCamLocs)

        # Render both in the beginning
        self.ui.renderGroundTruthCheckBox.setChecked(True)
        self.ui.renderModeledCheckBox.setChecked(True)

        self.ui.renderGroundTruthCheckBox.stateChanged.connect(
            self.setSceneVisualsData)
        self.ui.renderModeledCheckBox.stateChanged.connect(
            self.setSceneVisualsData)

    # Create the 3d vispy widget and setup the camera
    def createVispyWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor=(28 / 255, 31 / 255, 36 / 255))
        self.ui.cameraRenderPlace.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.view.camera = 'turntable'  # scene.cameras.FlyCamera()  # or try 'arcball'

        s = STTransform(translate=(500, 500, 200), scale=(50, 50, 50, 1))

        centerOfMass = self.getCenterOfMass()
        self.view.camera.center = tuple(centerOfMass)
        self.view.camera.scale_factor = 1.0
        self.view.camera.update()

    # For rotating
    def getCenterOfMass(self):
        allPositions = [self.data.trueCamLocs[timestamp].translation
                        for timestamp in self.data.timestamps]
        return np.sum(allPositions, axis=0) / len(self.data.timestamps)

    # Get the camera location, including its translation and rotation
    def getRenders(self, cameraLocations):
        cameras = []
        lines = []

        for timestamps in self.data.timestamps[:-1]:
            currCamera = cameraLocations[timestamps]

            if not currCamera:
                continue

            # Use the forward vector (Unity mindset) to get a point which the camera is directed to
            rotated = currCamera.quaternion.rotate(np.array([0, 0, 0.04]))

            # Add the data
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

    # Clear the screen before handling the checkbox
    def clearScreen(self):
        emptyData = np.empty((0, 3))

        self.trueScatter.set_data(np.empty((0, 3)), face_color=(1, 1, 1, 1))
        self.modeledScatter.set_data(np.empty((0, 3)), face_color=(1, 1, 1, 1))

        self.trueLines.set_data(np.empty((0, 3)), color=(1, 1, 1, 1))
        self.modeledLines.set_data(np.empty((0, 3)), color=(1, 1, 1, 1))

    # Connect the rangeslider
    def getSlicedRenders(self, cams, directions, col1, col2):
        start = self.ui.start
        end = self.ui.end
        currCameras = cams[start: end]
        currDirections = directions[start * 2: end * 2]

        pointColors = self.getColours(len(currCameras), col1, col2)
        lineColors = np.repeat(pointColors, 2, axis=0)

        return currCameras, currDirections, pointColors, lineColors

    # Rendering the true cameras
    def renderTrueCameras(self):
        trueData = self.getSlicedRenders(
            self.trueCameras, self.trueDirections, 'blue', 'purple')
        currCams, currDirects, pointColors, lineColors = trueData
        self.trueScatter.set_data(currCams, edge_color=None,
                                  face_color=pointColors, size=10, scaling=False)
        self.trueLines.set_data(
            pos=currDirects, color=lineColors, connect="segments")

    # Rendering the modeled cameras
    def renderModeledCameras(self):
        modeledData = self.getSlicedRenders(
            self.modeledCameras, self.modeledDirections, 'yellow', 'green')
        currCams, currDirects, pointColors, lineColors = modeledData
        self.modeledScatter.set_data(currCams, edge_color=None,
                                     face_color=pointColors, size=10, scaling=False)
        self.modeledLines.set_data(
            pos=currDirects, color=lineColors, connect="segments")

    # Connection point from the main screen
    def setSceneVisualsData(self, newSelect=False):
        self.clearScreen()
        amount = self.ui.end - self.ui.start
        if amount <= 1:
            return

        if self.ui.renderGroundTruthCheckBox.isChecked():
            self.renderTrueCameras()

        if self.ui.renderModeledCheckBox.isChecked():
            self.renderModeledCameras()
            pass
