import os
from src.data.extractors.dataExtractor import DataExtractor
from src.ui.videoPageHandler import VideoPageHandler
from src.ui.pointCloudPageHandler import PointCloudPageHandler
from src.ui.cameraPageHandler import CameraPageHandler
from src.ui.chartPageHandler import ChartPageHandler
from src.camera import CameraParameters
from src.constants import DEFAULT_DATASET_DIRECTORY, DEFAULT_CAMERA_PARAMETERS
from src.constants import VIDEO_PAGE_INDEX, POINT_CLOUD_PAGE_INDEX, CAMERA_PAGE_INDEX, CHARTS_PAGE_INDEX
from src.ui.rangeslider import QRangeSlider


class SLAMWindow:
    def __init__(self, ui):
        self.ui = ui
        self.data = None

        self.createRangeSliderWidget()
        self.connectLeftFrameButtons()
    # Create the range slider widget

    def createRangeSliderWidget(self):
        self.rangeSlider = QRangeSlider()
        self.rangeSlider.setMaximumHeight(20)
        self.ui.rangeSliderBar.layout().addWidget(self.rangeSlider)

    # To make the buttons in the left menu work

    def connectLeftFrameButtons(self):
        # For changing the stackedwidget index

        self.pages = [self.ui.videoButton]
        self.ui.videoButton.clicked.connect(
            lambda: self.setMainStackedPage(VIDEO_PAGE_INDEX))
        self.ui.pointCloudButton.clicked.connect(
            lambda: self.setMainStackedPage(POINT_CLOUD_PAGE_INDEX))
        self.ui.camera3dButton.clicked.connect(
            lambda: self.setMainStackedPage(CAMERA_PAGE_INDEX))
        self.ui.chartButton.clicked.connect(
            lambda: self.setMainStackedPage(CHARTS_PAGE_INDEX))

        # Loading in the default dataset
        self.ui.uploadDefaultDatasetButton.clicked.connect(
            self.loadDefaultDirectory)

    # Load in a default dataset

    def loadDefaultDirectory(self):
        if(self.data):
            return

        self.loadDirectory(DEFAULT_DATASET_DIRECTORY)

    # Load in the data, and setup the widgets

    def loadDirectory(self, path):

        self.data = DataExtractor.loadDirectory(
            path, DEFAULT_CAMERA_PARAMETERS)

        print("Loaded in all data")
        self.ui.notificationLabel.setText("Loaded dataset: {}".format(path))

        self.ui.start = 0
        self.ui.end = len(self.data.timestamps)

        self.videoPageHandler = VideoPageHandler(self.ui, self.data)
        self.pointCloudPageHandler = PointCloudPageHandler(self.ui, self.data)
        self.cameraPageHandler = CameraPageHandler(self.ui, self.data)
        self.chartPageHandler = ChartPageHandler(self.ui, self.data)

        self.updateablePages = [None, self.videoPageHandler, self.pointCloudPageHandler,
                                self.cameraPageHandler, self.chartPageHandler]

        self.connectRangeSlider(len(self.data.timestamps))
        self.updateRangeSlider()

    def connectRangeSlider(self, cameraAmount):
        self.rangeSlider.setMin(0)
        self.rangeSlider.setMax(cameraAmount)

        self.rangeSlider.setStart(0)
        self.rangeSlider.setEnd(cameraAmount)

        self.rangeSlider.startValueChanged.connect(self.updateRangeSlider)
        self.rangeSlider.endValueChanged.connect(self.updateRangeSlider)

    def updateRangeSlider(self):
        start = self.rangeSlider.start()
        end = self.rangeSlider.end()
        self.ui.start = start
        self.ui.end = end

        self.updateCurrentPage(False)

    # Otherwise the vispy module causes a memory leak
    def updateCurrentPage(self, newSelect):
        currIndex = self.ui.mainStackedWidget.currentIndex()
        currPage = self.updateablePages[currIndex]

        if currPage:
            currPage.setSceneVisualsData(newSelect)

    # Change the stackedWidget index

    def setMainStackedPage(self, index):
        if not self.data:
            print("Load in data first")
            return

        self.ui.mainStackedWidget.setCurrentIndex(index)
        self.updateCurrentPage(True)
