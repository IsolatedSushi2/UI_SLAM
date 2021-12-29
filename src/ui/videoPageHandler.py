from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
from src.constants import VIDEO_PAGE_INDEX


class VideoPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0

        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1000 // 30)

    # Go trough the images
    def updateFrame(self):

        # Disable when not using the page (less computation and avoids the vispy memory leak bug)
        if self.ui.mainStackedWidget.currentIndex() != VIDEO_PAGE_INDEX:
            return
        
        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]
        
        currRGBPixMap = self.cv2ToQPixmap(currRGBImage, QImage.Format_RGB888)
        currDepthPixMap = self.cv2ToQPixmap(np.array(currDepthImage, dtype=np.uint16), QImage.Format_Grayscale16) # Specify 

        self.ui.rgbImage.setPixmap(currRGBPixMap)
        self.ui.depthImage.setPixmap(currDepthPixMap)

        # Update frame
        self.currentFrameIndex = (self.currentFrameIndex + 1) % len(self.data.timestamps)

    # For translating numpy array to Pil image (don't want to keep everything in memory)
    def cv2ToQPixmap(self, currImage, imageFormat):
        height, width = (currImage.shape[0], currImage.shape[1])
        return QPixmap.fromImage(QImage(currImage, width, height, imageFormat))
