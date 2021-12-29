import os 
from src.datareader import DataReader
from src.ui.videoPageHandler import VideoPageHandler
from src.ui.pointCloudPageHandler import PointCloudPageHandler
from src.ui.cameraPageHandler import CameraPageHandler
from src.camera import CameraParameters

from src.constants import DEFAULT_DATASET_DIRECTORY, DEFAULT_CAMERA_PARAMETERS
from src.constants import VIDEO_PAGE_INDEX, POINT_CLOUD_PAGE_INDEX, CAMERA_PAGE_INDEX
cwd = os.getcwd()



class SLAM:
    def __init__(self, ui):
        self.ui = ui
        self.data = None

        self.connectLeftFrameButtons()
        self.loadDefaultDirectory()

    # To make the buttons in the left menu work
    def connectLeftFrameButtons(self):
        # For changing the stackedwidget index
        self.ui.videoButton.clicked.connect(lambda: self.setMainStackedPage(VIDEO_PAGE_INDEX))
        self.ui.pointCloudButton.clicked.connect(lambda: self.setMainStackedPage(POINT_CLOUD_PAGE_INDEX))
        self.ui.camera3dButton.clicked.connect(lambda: self.setMainStackedPage(CAMERA_PAGE_INDEX))

        # Loading in the default dataset
        self.ui.uploadDefaultDatasetButton.clicked.connect(self.loadDefaultDirectory)

    # Load in a default dataset
    def loadDefaultDirectory(self):
        if(self.data):
            return

        self.loadDirectory(DEFAULT_DATASET_DIRECTORY)

    # Load in the data, and setup the widgets
    def loadDirectory(self, path):

        self.data = DataReader().loadDirectory(path)

        print("Loaded in all data")
        self.ui.notificationLabel.setText("Loaded dataset: {}".format(path))

        self.videoPageHandler = VideoPageHandler(self.ui, self.data)
        self.pointCloudPageHandler = PointCloudPageHandler(self.ui, self.data, DEFAULT_CAMERA_PARAMETERS)
        self.cameraPageHandler = CameraPageHandler(self.ui, self.data)

    # Change the stackedWidget index
    def setMainStackedPage(self, index):
        self.ui.mainStackedWidget.setCurrentIndex(index)