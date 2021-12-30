import cv2
import numpy as np
from math import atan2, asin
import open3d as o3d
from src.constants import LOWES_RATIO_AMOUNT


class Frame:
    def __init__(self, timestamp, rgbImage, depthImage, cameraParams, keypointFinder=cv2.ORB_create(1000)):
        self.timestamp = timestamp
        self.rgbImage = rgbImage
        self.depthImage = depthImage
        self.kps, self.desc = self.findKeypointsInImage(keypointFinder)
        self.camParams = cameraParams

    def findKeypointsInImage(self, keypointFinder):
        kp, des = keypointFinder.detectAndCompute(self.rgbImage, None)
        return kp, des

    def getRenderedImages(self, drawKeypoints):
        rgbImage = cv2.drawKeypoints(
            self.rgbImage, self.kps, None, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT) if drawKeypoints else self.rgbImage
        return (rgbImage, self.depthImage)

    # Can be removed
    def show(self, drawKeypoints=True):
        rgbImage, depthImage = self.getRenderedImages(drawKeypoints)
        renderedImage = np.hstack((rgbImage, depthImage))
        cv2.imshow("Frame", renderedImage)
        cv2.waitKey(0)


class StereoFrame:
    def __init__(self, frame1, frame2, matchingAlg=cv2.BFMatcher(cv2.NORM_HAMMING)):
        self.frame1 = frame1
        self.frame2 = frame2
        self.matcher = matchingAlg
        self.matches, self.pts1, self.pts2 = self.getMatches()

    def getMatches(self):
        matches = self.matcher.match(self.frame1.desc, self.frame2.desc)
        matches = sorted(matches, key=lambda x: x.distance)[:LOWES_RATIO_AMOUNT]

        # Replace for loop by numpy (significantly faster)
        pts1 = []
        pts2 = []
        # ratio test as per Lowe's paper
        for m in matches:
            pts2.append(self.frame2.kps[m.trainIdx].pt)
            pts1.append(self.frame1.kps[m.queryIdx].pt)

        pts1 = np.float64(pts1)
        pts2 = np.float64(pts2)

        return matches, pts1, pts2

    def getFundamentalMatrix(self):
        return cv2.findFundamentalMat(self.pts1, self.pts2, cv2.FM_LMEDS)

    def getEssentialMatrix(self):
        F, _ = self.getFundamentalMatrix()
        K = self.frame1.camParams.getKMatrix()

        return K.T * F * K

    def getRenderedImages(self, drawKeypoints=True):
        rgbimg1, depthimg1 = self.frame1.getRenderedImages(drawKeypoints)
        rgbimg2, depthimg2 = self.frame2.getRenderedImages(drawKeypoints)

        img = cv2.drawMatches(self.frame1.rgbImage, self.frame1.kps,
                              self.frame2.rgbImage, self.frame2.kps, self.matches, None)

        depthImages = np.hstack((depthimg1, depthimg2))

        return img, depthImages

    # Can be removed
    def show(self, drawKeypoints=True):
        img = self.getRenderedImage(drawKeypoints)
        cv2.imshow("StereoFrame", img)
        cv2.waitKey(0)
