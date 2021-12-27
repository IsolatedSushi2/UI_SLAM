import os 
from src.datareader import DataReader
from src.ui.videoPageHandler import VideoPageHandler
cwd = os.getcwd()

DEFAULT_DATASET_DIRECTORY = os.path.join(os.getcwd(),"data","rgbd_dataset_freiburg1_360")
print(DEFAULT_DATASET_DIRECTORY)
class SLAM():
    def __init__(self, ui):
        self.ui = ui
        self.data = None

        self.videoPageHandler = None

        self.connectLeftFrameButtons()

    def connectLeftFrameButtons(self):
        # For changing the stackedwidget index
        self.ui.videoButton.clicked.connect(lambda: self.setMainStackedPage(1))
        self.ui.pointCloudButton.clicked.connect(lambda: self.setMainStackedPage(2))

        # Loading in the default dataset
        self.ui.uploadDefaultDatasetButton.clicked.connect(self.loadDefaultDirectory)


    def loadDefaultDirectory(self):
        if(self.data):
            return

        self.loadDirectory(DEFAULT_DATASET_DIRECTORY)

        
    def loadDirectory(self, path):
        self.data = DataReader().loadDirectory(path)
        self.videoPageHandler = VideoPageHandler(self.ui, self.data)
        print("Loaded in all data")

    def setMainStackedPage(self, index):
        self.ui.mainStackedWidget.setCurrentIndex(index)