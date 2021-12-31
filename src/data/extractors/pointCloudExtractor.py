from src.constants import MAX_POINTS_PER_CLOUD_RATIO
import numpy as np


class PointCloudExtractor:

    @staticmethod
    def translate_point_cloud(positions, colors, cameraLoc):
        translation = cameraLoc.translation
        rotationMatrix = cameraLoc.quaternion.rotation_matrix

        transformedPositions = rotationMatrix.dot(positions.T).T + translation

        return transformedPositions, colors

    @staticmethod
    # , sampledDepth, cameraLoc, camParams, u, v):
    def generate_point_cloud_improved(rgb, depth, indices, camParams):

        # Note, these are also u and v, since they are indexing by the pixels
        rowIndices, columnIndices = indices

        # Get the sampled values
        sampledRGB = rgb[rowIndices, columnIndices]
        sampledDepth = depth[rowIndices, columnIndices]

        # Delete those which have a depth value of 0 (are faulty)
        depthMask = sampledDepth != 0

        u = rowIndices[depthMask]
        v = columnIndices[depthMask]

        colors = sampledRGB[depthMask] / 255  # Need value between 0 and 1
        finalDepth = sampledDepth[depthMask]

        Z = finalDepth / camParams.depthScalingFactor
        X = np.multiply(v - camParams.centerx, Z / camParams.focalx)
        Y = np.multiply(u - camParams.centery, Z / camParams.focaly)

        return np.column_stack((X, Y, Z)), colors

    # Inspired from the given generate_pointcloud.py, but optimised because it was way too slow

    @staticmethod
    def generate_point_cloud(rgbImage, depthImage, cameraLoc, camParams):
        translation = cameraLoc.translation
        rotationMatrix = cameraLoc.quaternion.rotation_matrix

        depthMask = depthImage != 0
        width, height = depthImage.shape

        colors = rgbImage[depthMask] / 255  # Need value between 0 and 1
        depth = depthImage[depthMask]

        # TODO, do the sampling before extracting the positions
        # Optimized numpy implementation instead of the slow for loops from the datasets authors
        Z = depth / camParams.depthScalingFactor
        u = np.tile(np.arange(width), (height, 1)).T[depthMask]
        v = np.tile(np.arange(height), (width, 1))[depthMask]
        X = np.multiply(v - camParams.centerx, Z / camParams.focalx)
        Y = np.multiply(u - camParams.centery, Z / camParams.focaly)

        positions = np.column_stack((X, Y, Z))
        transformedPositions = rotationMatrix.dot(
            positions.T).T + translation

        return PointCloudExtractor.samplePoints(transformedPositions, colors, MAX_POINTS_PER_CLOUD_RATIO)

    # Does contain duplicates
    @staticmethod
    def getSamplePointsIndices(width, height, ratio):
        sampleNumber = int(ratio * width * height)

        sampledX = np.random.choice(
            np.arange(width), sampleNumber, replace=True)
        sampledY = np.random.choice(
            np.arange(height), sampleNumber, replace=True)

        return sampledX, sampledY
