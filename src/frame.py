import cv2
import numpy as np
from math import atan2, asin
import open3d as o3d
from src.constants import MAX_MATCH_AMOUNT, DRAW_KEYPOINTS_MATCHES, KEYPOINT_FINDER, MATCHING_ALG


class Frame:
    def __init__(self, timestamp, rgbImage, depthImage, cameraParams):
        self.timestamp = timestamp
        self.rgbImage = rgbImage
        self.depthImage = depthImage
        self.keypoints, self.kps, self.desc, self.roundedKeyPoints = self.findKeypointsInImageBefore(
            KEYPOINT_FINDER)

        self.camParams = cameraParams

        self.relativeKPSPointCloud = None

    def clearImagesFromMemory(self):
        del self.rgbImage
        del self.depthImage

    # First method, specifying a mask deleting the invalid depth values beforehand
    def findKeypointsInImageBefore(self, keypointFinder):
        depthMask = np.asarray(self.depthImage != 0, dtype=np.uint8)
        # Find keypoints
        kps, des = keypointFinder.detectAndCompute(
            self.rgbImage, mask=depthMask)

        kPoints = np.array([keypoint.pt for keypoint in kps])
        roundedKpoints = np.asarray(np.rint(kPoints), dtype=np.uint16)

        # Return values with the depth mask
        return np.array(kps), kPoints, des, roundedKpoints

    # Second method, specifying a mask deleting the invalid depth values afterwards

    def findKeypointsInImageAfter(self, keypointFinder):

        # Find keypoints
        kps, des = keypointFinder.detectAndCompute(self.rgbImage, None)

        # Get the points and rounded points (For indexing the depth map)
        kPoints = np.array([keypoint.pt for keypoint in kps])
        roundedKpoints = np.asarray(np.rint(kPoints), dtype=np.uint16)

        # Check which ones have a depth value associated
        kpsDepthMask = self.depthImage[roundedKpoints[:,
                                                      1], roundedKpoints[:, 0]] != 0
        print(np.count_nonzero(~kpsDepthMask))

        # Return values with the depth mask
        return np.array(kps)[kpsDepthMask], kPoints[kpsDepthMask], des[kpsDepthMask], roundedKpoints[kpsDepthMask]

    def getRenderedImages(self):
        rgbImage = cv2.drawKeypoints(
            self.rgbImage, self.keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT) if DRAW_KEYPOINTS_MATCHES else self.rgbImage
        return (rgbImage, self.depthImage)


# (stereoframe can be referenced by the timestamp of the first frame)
class StereoFrame:
    def __init__(self, frame1, frame2):
        self.frame1 = frame1
        self.frame2 = frame2

        self.camParams = self.frame1.camParams

        self.frame1KPS = None
        self.frame2KPS = None

        self.K = frame1.camParams.getKMatrix()
        self.matches, self.pts1, self.pts2 = self.getMatches(MATCHING_ALG)

    def getMatches(self, matcher):
        matches = matcher.match(self.frame1.desc, self.frame2.desc)
        matches = sorted(matches, key=lambda x: x.distance)
        matches = matches[:MAX_MATCH_AMOUNT]

        frame1Indices = np.array(
            [match.queryIdx for match in matches], dtype=np.int16)
        frame2Indices = np.array(
            [match.trainIdx for match in matches], dtype=np.int16)

        pts1 = np.float64(self.frame1.kps[frame1Indices])
        pts2 = np.float64(self.frame2.kps[frame2Indices])

        # Just use the pointclouds used in matches

        self.frame1KPS = self.frame1.relativeKPSPointCloud[frame1Indices]
        self.frame2KPS = self.frame2.relativeKPSPointCloud[frame2Indices]

        return matches, pts1, pts2

    def getFundamentalMatrix(self):
        return cv2.findFundamentalMat(self.pts1, self.pts2, cv2.FM_LMEDS)

    def getEssentialMatrix(self):
        F, _ = self.getFundamentalMatrix()
        K = self.frame1.camParams.getKMatrix()

        return K.T * F * K

    def getRenderedImages(self):
        rgbimg1, depthimg1 = self.frame1.getRenderedImages()
        rgbimg2, depthimg2 = self.frame2.getRenderedImages()

        # Render the rgb images with or without keypoints and matches
        if DRAW_KEYPOINTS_MATCHES:
            rgbImages = cv2.drawMatches(self.frame1.rgbImage, self.frame1.keypoints,
                                        self.frame2.rgbImage, self.frame2.keypoints, self.matches, None)
        else:
            rgbImages = np.hstack((rgbimg1, rgbimg2))

        depthImages = np.hstack((depthimg1, depthimg2))

        return rgbImages, depthImages

    # Can be removed
    def show(self, drawKeypoints=True):
        img = self.getRenderedImage(drawKeypoints)
        cv2.imshow("StereoFrame", img)
        cv2.waitKey(0)
