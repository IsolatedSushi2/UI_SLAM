from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

class VideoPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0

        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1000 // 60)

    def updateFrame(self):
        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]
        
        currPixMap = self.cv2ToQPixmap(currRGBImage,QImage.Format_RGB888)
        self.ui.rgbImage.setPixmap(currPixMap)

        currPixMap = self.cv2ToQPixmap(currDepthImage,QImage.Format_RGB16)
        self.ui.depthImage.setPixmap(currPixMap)

        self.currentFrameIndex = (self.currentFrameIndex + 1) % len(self.data.timestamps)

    def cv2ToQPixmap(self, currImage, imageFormat):
        height, width = (currImage.shape[0], currImage.shape[1])
        
        #bytesPerLine = {QImage.Format_RGB888:3, QImage.Format_Grayscale16:2}[imageFormat] * width
        return QPixmap.fromImage(QImage(currImage, width, height, imageFormat))
