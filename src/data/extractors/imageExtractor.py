from src.constants import STORE_ALL_IMAGES
from src.frame import Frame, StereoFrame


# Get the frames
class ImageExtractor:

    @staticmethod
    def getFrame(timestamp, rgbImg, depthImg, camParams):
        returnFrame = Frame(timestamp, rgbImg, depthImg, camParams)

        # The ability to clear from memory
        if not STORE_ALL_IMAGES:
            returnFrame.clearImagesFromMemory()

        return returnFrame

    @staticmethod
    def getStereoFrame(frame1, frame2):
        # TODO, figure out the matching algoritm
        return StereoFrame(frame1, frame2)