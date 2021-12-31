from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
from src.constants import VIDEO_PAGE_INDEX, STORE_ALL_IMAGES
from src.frame import Frame, StereoFrame

class VideoPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0 

        # First frame
        self.updateFrame(True)

        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1000 // 10)

    # Go trough the images
    def updateFrame(self, force=False):

        # Disable when not using the page (less computation and avoids the vispy memory leak bug)
        if self.ui.mainStackedWidget.currentIndex() != VIDEO_PAGE_INDEX and not force:
            return

        # The images are not stored
        if not STORE_ALL_IMAGES:
            return

        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        stereoFrame = self.data.stereoFrames[currTimestamp]

        renderedStereoRGB, renderedStereoDepth = stereoFrame.getRenderedImages()

        currRGBPixMap = self.cv2ToQPixmap(renderedStereoRGB, QImage.Format_RGB888)
        currDepthPixMap = self.cv2ToQPixmap(np.array(renderedStereoDepth, dtype=np.uint16), QImage.Format_Grayscale16)  # Specify

        self.ui.rgbImage.setPixmap(currRGBPixMap)
        self.ui.depthImage.setPixmap(currDepthPixMap)

        # Update frame
        stereoFrameAmount = (len(self.data.timestamps) - 1)
        self.currentFrameIndex = (self.currentFrameIndex + 1) % stereoFrameAmount

    # For translating numpy array to Pil image (don't want to keep everything in memory)
    def cv2ToQPixmap(self, currImage, imageFormat):
        height, width = (currImage.shape[0], currImage.shape[1])
        return QPixmap.fromImage(QImage(currImage, width, height, imageFormat))
