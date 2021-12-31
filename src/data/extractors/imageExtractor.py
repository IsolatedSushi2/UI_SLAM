from src.constants import STORE_ALL_IMAGES
from src.frame import Frame, StereoFrame


class ImageExtractor:

    @staticmethod
    def getFrame(timestamp, rgbImg, depthImg, camParams):
        # TODO, figure out the keypointFinder algorithm
        returnFrame = Frame(timestamp, rgbImg, depthImg, camParams)
        
        if not STORE_ALL_IMAGES:
            returnFrame.clearImagesFromMemory()

        return returnFrame

    @staticmethod
    def getStereoFrame(frame1, frame2):
        # TODO, figure out the matching algoritm
        return StereoFrame(frame1, frame2)


