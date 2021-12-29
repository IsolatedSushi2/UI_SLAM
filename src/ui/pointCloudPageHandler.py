import numpy as np
from vispy import scene
from vispy.scene import visuals
from PyQt5.QtCore import QTimer
import gc
from pyquaternion import Quaternion
class PointCloudPageHandler:
    def __init__(self, ui, dataObject, cameraParameters):
        self.ui = ui
        self.data = dataObject
        self.camParams = cameraParameters


        self.originShift = self.data.groundTruth[self.data.timestamps[0]].translation

        self.allPos = np.empty((0,3))
        self.allColors = np.empty((0,3))

        self.currentFrameIndex = 0

        self.setupWidget()
        #self.updateFrame()

        
        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(5000)

    def setupWidget(self):
        self.canvas = scene.SceneCanvas(
            keys='interactive', size=(600, 600), show=True, bgcolor='black', vsync=False)
        self.ui.pointCloudPage.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()

        self.scatter = visuals.Markers()
        self.scatter.set_gl_state('translucent',depth_test=False)
        self.scatter.set_data(pos=  np.random.normal(size=(1, 3), scale=0.2), edge_color=None, face_color=(1, 1, 1, .5), size=10,scaling=True)

        self.view.add(self.scatter)

        self.view.camera = 'turntable'#scene.cameras.FlyCamera()  # or try 'arcball'

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=self.view.scene)

    def generate_pointcloud(self, timestamp, rotationMatrix):
        print("Generating")
        focalLength = 525.0
        centerX = 319.5
        centerY = 239.5
        scalingFactor = 5000.0

        rgb = self.data.rgbImages[timestamp]
        depth = self.data.depthImages[timestamp]
        points = []
        colors = []
        for v in range(rgb.size[1]):
            for u in range(rgb.size[0]):
                color = rgb.getpixel((u,v))
                Z = depth.getpixel((u,v)) / scalingFactor
                if Z==0: continue
                X = (u - centerX) * Z / focalLength
                Y = (v - centerY) * Z / focalLength
                points.append(np.array([X,Y,Z]))
                colors.append(np.array(color))
        print("Finished generating")

        return rotationMatrix.dot(np.array(points).T).T + self.data.groundTruth[timestamp].translation, np.array(colors) / 255

    def updateFrame(self):
        gc.collect()
        print("Collect")

        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]



        x, y, z, w = tuple(self.data.groundTruth[currTimestamp].quaternion)
        quaternion = Quaternion(x=x, y=y, z=z,w=w)
        pos, colors = self.generate_pointcloud(currTimestamp, quaternion.rotation_matrix)
        print(colors[0])

        self.allPos = np.concatenate((self.allPos, pos))
        self.allColors =np.concatenate((self.allColors, colors))

        self.canvas.measure_fps()

        #print(pos.shape)
        #self.scatter.update()
        self.scatter.set_data(pos = self.allPos, edge_width=0, face_color=self.allColors, size=1, scaling=False)
        self.currentFrameIndex = (self.currentFrameIndex + 10) % len(self.data.timestamps)




