import open3d as o3d
import numpy as np
from vispy import scene
from vispy.scene import visuals
from PyQt5.QtCore import QTimer
import gc

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
        self.updateFrame()

        
        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(2000)

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


    def updateFrame(self):
        gc.collect()
        print("Collect")

        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]


        print(currRGBImage)

        return
        color_raw = o3d.geometry.Image(currRGBImage.astype(np.uint8))
        depth_raw = o3d.geometry.Image(currDepthImage.astype(np.uint8))

        rgbd_image = o3d.geometry.RGBDImage.create_from_tum_format(color_raw, depth_raw, convert_rgb_to_intensity=False)
        intr = o3d.open3d.camera.PinholeCameraIntrinsic(self.camParams.width, self.camParams.height, fx=self.camParams.focalx, fy=self.camParams.focaly, cx=self.camParams.centerx, cy=self.camParams.centery)

        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intr)

        #R = pcd.get_rotation_matrix_from_xyz((-np.pi/2.0, 0, 0))
        #pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        pcd.scale(5000, center=[0,0,0])

        print(pcd.points[0])

        x, y, z, w = tuple(self.data.groundTruth[currTimestamp].quaternion)
        R = pcd.get_rotation_matrix_from_quaternion(np.array([w,x,y,z]))
        pcd.rotate(R)

        pcd.translate(self.data.groundTruth[currTimestamp].translation) #- self.originShift)

        pos = np.asarray(pcd.points) 
        colors = np.asarray(pcd.colors)
        self.allPos = np.concatenate((self.allPos, pos))
        self.allColors =np.concatenate((self.allColors, colors))

        self.canvas.measure_fps()

        #print(pos.shape)
        #self.scatter.update()
        self.scatter.set_data(pos = self.allPos, edge_width=0, face_color=self.allColors, size=1, scaling=False)
        self.currentFrameIndex = (self.currentFrameIndex + 10) % len(self.data.timestamps)




