from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2

class VideoPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0

        #Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1000 // 30)

    def updateFrame(self):
        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]
        
        currPixMap = self.cv2ToQPixmap(currRGBImage)
        self.ui.rgbImage.setPixmap(currPixMap)

        currPixMap = self.cv2ToQPixmap(currDepthImage)
        self.ui.depthImage.setPixmap(currPixMap)

        self.currentFrameIndex = (self.currentFrameIndex + 1) % len(self.data.timestamps)

    def cv2ToQPixmap(self, currImage):
        height, width, channel = currImage.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(currImage.data, width, height, bytesPerLine, QImage.Format_RGB888))
