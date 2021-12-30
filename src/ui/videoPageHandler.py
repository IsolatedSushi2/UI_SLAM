from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
from src.constants import VIDEO_PAGE_INDEX
from src.frame import Frame, StereoFrame

class VideoPageHandler:
    def __init__(self, ui, dataObject, cameraParameters):
        self.ui = ui
        self.data = dataObject

        self.currentFrameIndex = 0 
        self.camParams = cameraParameters

        # Update Timer for the video
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1000 // 10)

    # Go trough the images
    def updateFrame(self):

        # Disable when not using the page (less computation and avoids the vispy memory leak bug)
        if self.ui.mainStackedWidget.currentIndex() != VIDEO_PAGE_INDEX:
            return

        currTimestamp = self.data.timestamps[self.currentFrameIndex]
        currTimestamp2 = self.data.timestamps[self.currentFrameIndex + 1]

        currRGBImage = self.data.rgbImages[currTimestamp]
        currDepthImage = self.data.depthImages[currTimestamp]

        currRGBImage2 = self.data.rgbImages[currTimestamp2]
        currDepthImage2 = self.data.depthImages[currTimestamp2]

        frame1 = Frame(currTimestamp, currRGBImage, currDepthImage, self.camParams)
        frame2 = Frame(currTimestamp2, currRGBImage2, currDepthImage2, self.camParams)
        
        stereoFrame = StereoFrame(frame1, frame2)

        renderedStereoRGB, renderedStereoDepth = stereoFrame.getRenderedImages()

        currRGBPixMap = self.cv2ToQPixmap(renderedStereoRGB, QImage.Format_RGB888)
        currDepthPixMap = self.cv2ToQPixmap(np.array(renderedStereoDepth, dtype=np.uint16), QImage.Format_Grayscale16)  # Specify

        self.ui.rgbImage.setPixmap(currRGBPixMap)
        self.ui.depthImage.setPixmap(currDepthPixMap)


        # Update frame
        self.currentFrameIndex = (self.currentFrameIndex + 2) % len(self.data.timestamps)

    # For translating numpy array to Pil image (don't want to keep everything in memory)
    def cv2ToQPixmap(self, currImage, imageFormat):
        height, width = (currImage.shape[0], currImage.shape[1])
        return QPixmap.fromImage(QImage(currImage, width, height, imageFormat))
