import numpy as np
from vispy import scene
from vispy.scene import visuals
from colour import Color
from pyquaternion import Quaternion

class CameraPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0

        self.createWidget()
        self.addSceneVisuals()
        self.setSceneVisualsData()

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

    # Create the 3d vispy widget
    def createWidget(self):
        self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600), show=True, bgcolor='black')
        self.ui.camera3dPage.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.view.camera = 'turntable'  # scene.cameras.FlyCamera()  # or try 'arcball'

    def addSceneVisuals(self):
        # For the camera positions
        self.scatter = visuals.Markers()
        self.scatter.set_gl_state('translucent', depth_test=False) # TODO, find wtf this does exactly (something is getting messed up when using anti aliasing)
        self.view.add(self.scatter)

        # For the line positions
        self.lines = visuals.Line()
        self.view.add(self.lines)

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)
    
    def setSceneVisualsData(self):
        cameras, lines = self.getRenders()        
        colors = self.getColours(len(cameras))

        self.scatter.set_data(cameras, edge_color=None, face_color=colors, size=10, scaling=False)
        self.lines.set_data(pos=lines, color=np.repeat(colors, 2, axis=0), connect="segments")

        


