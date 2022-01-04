from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
from src.constants import VIDEO_PAGE_INDEX, STORE_ALL_IMAGES
from src.frame import Frame, StereoFrame


# Handles the video page
class VideoPageHandler:
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject
        self.lastIndex = -1

    def getRenders(self):
        currentIndex = max(self.ui.start - 1, 0)
        currTimestamp = self.data.timestamps[currentIndex]
        stereoFrame = self.data.stereoFrames[currTimestamp]

        renderedStereoRGB, renderedStereoDepth = stereoFrame.getRenderedImages()
        return renderedStereoRGB, renderedStereoDepth

    # Go trough the images
    def RenderImages(self, renderedStereoRGB, renderedStereoDepth):
        currRGBPixMap = self.cv2ToQPixmap(
            renderedStereoRGB, QImage.Format_RGB888)
        currDepthPixMap = self.cv2ToQPixmap(np.array(
            renderedStereoDepth, dtype=np.uint16), QImage.Format_Grayscale16)  # Specify

        self.ui.rgbImage.setPixmap(currRGBPixMap)
        self.ui.depthImage.setPixmap(currDepthPixMap)

    # For translating numpy array to Pil image (don't want to keep everything in memory)
    def cv2ToQPixmap(self, currImage, imageFormat):
        height, width = (currImage.shape[0], currImage.shape[1])
        return QPixmap.fromImage(QImage(currImage, width, height, imageFormat))

    def setSceneVisualsData(self, newSelect=False):

        # The images are not stored
        if not STORE_ALL_IMAGES:
            return

        # For solving the jitter issues
        if self.ui.start == self.lastIndex:
            return

        self.lastIndex = self.ui.start
        rgb, depth = self.getRenders()
        self.RenderImages(rgb, depth)
