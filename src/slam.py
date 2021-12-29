import os 
from src.datareader import DataReader
from src.ui.videoPageHandler import VideoPageHandler
from src.ui.pointCloudPageHandler import PointCloudPageHandler
from src.ui.cameraPageHandler import CameraPageHandler
from src.camera import CameraParameters
cwd = os.getcwd()

DEFAULT_DATASET_DIRECTORY = os.path.join(os.getcwd(),"data","rgbd_dataset_freiburg1_360")
DEFAULT_CAMERAPARAMETERS = CameraParameters(640, 480, 525, 525, 319.5, 239.5)

class SLAM:
    def __init__(self, ui):
        self.ui = ui
        self.data = None

        self.videoPageHandler = None
        self.pointCloudPageHandler = None

        self.connectLeftFrameButtons()
        self.loadDefaultDirectory()

    def connectLeftFrameButtons(self):
        # For changing the stackedwidget index
        self.ui.videoButton.clicked.connect(lambda: self.setMainStackedPage(1))
        self.ui.pointCloudButton.clicked.connect(lambda: self.setMainStackedPage(2))
        self.ui.camera3dButton.clicked.connect(lambda: self.setMainStackedPage(3))

        # Loading in the default dataset
        self.ui.uploadDefaultDatasetButton.clicked.connect(self.loadDefaultDirectory)

    def loadDefaultDirectory(self):
        if(self.data):
            return

        self.loadDirectory(DEFAULT_DATASET_DIRECTORY)

    def loadDirectory(self, path):

        self.data = DataReader().loadDirectory(path)

        print("Loaded in all data")

        self.videoPageHandler = VideoPageHandler(self.ui, self.data)
        self.pointCloudPageHandler = PointCloudPageHandler(self.ui, self.data, DEFAULT_CAMERAPARAMETERS)
        self.cameraPageHandler = CameraPageHandler(self.ui, self.data)

    def setMainStackedPage(self, index):
        self.ui.mainStackedWidget.setCurrentIndex(index)