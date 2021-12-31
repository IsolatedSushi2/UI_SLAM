from src.constants import MAX_POINTS_PER_CLOUD_RATIO
import numpy as np

class PointCloudExtractor:

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

    @staticmethod
    def samplePoints(positions, colors, sampleRatio):
        sampledPoints = int(len(positions) * sampleRatio)
        sampledIndices = np.random.choice(
            range(len(positions)), sampledPoints, replace=False)

        return positions[sampledIndices], colors[sampledIndices]