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

        self.setupWidget()
        #self.updateFrame()

    def getRenders(self):
        
        cameras = []
        lines = []

        for timestamps in self.data.groundTruth.keys():
            currGroundTruth = self.data.groundTruth[timestamps]

            x, y, z, w = tuple(currGroundTruth.quaternion)
            quaternion = Quaternion(w=w, x=x, y=y, z=z)

            rotated = quaternion.rotate(np.array([0, 0, 0.1]))

            cameras.append(currGroundTruth.translation)
            lines.append(currGroundTruth.translation)
            lines.append(rotated + currGroundTruth.translation)

        return np.array(cameras), np.array(lines)

    def getColours(self, amount):
        red = Color("blue")
        colors = list(red.range_to(Color("red"), amount))

        return np.asarray([color.rgb for color in colors])

    def setupWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor='black')
        self.ui.camera3dPage.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.scatter = visuals.Markers()
        self.lines = visuals.Line()

        self.scatter.set_gl_state('translucent',depth_test=False)

        cameras, lines = self.getRenders()
        
        colors = self.getColours(len(cameras))

        self.scatter.set_data(cameras, edge_color=None, face_color=colors, size=10,scaling=False)
        self.lines.set_data(pos =lines,color=np.repeat(colors,2,axis=0), connect="segments" )
        self.view.add(self.scatter)
        self.view.add(self.lines)

        self.view.camera = 'turntable'#scene.cameras.FlyCamera()  # or try 'arcball'

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)
