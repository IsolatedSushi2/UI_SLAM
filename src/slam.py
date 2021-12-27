import os 
cwd = os.getcwd()

DEFAULT_DATASET_DIRECTORY = os.path.join(os.getcwd(),"/data","/rgbd_dataset_freiburg2_xyz")

class SLAM():
    def __init__(self, ui):
        self.ui = ui

        self.connectLeftFrameButtons()

    def connectLeftFrameButtons(self):
        #For changing the stackedwidget index
        self.ui.videoButton.clicked.connect(lambda: self.setMainStackedPage(1))
        self.ui.pointCloudButton.clicked.connect(lambda: self.setMainStackedPage(2))

        #Loading in the directory

    def setMainStackedPage(self, index):
        self.ui.mainStackedWidget.setCurrentIndex(index)