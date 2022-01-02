from src.constants import MAX_POINTS_PER_CLOUD_RATIO
import numpy as np

# Contains useful functions for handling pointclouds
class PointCloudExtractor:

    # Translate the point cloud
    @staticmethod
    def translate_point_cloud(positions, colors, cameraLoc):
        translation = cameraLoc.translation
        rotationMatrix = cameraLoc.quaternion.rotation_matrix

        rotatedPoints = rotationMatrix.dot(positions.T).T
        transformedPositions = rotatedPoints + translation

        return transformedPositions, colors

    @staticmethod
    # Inspired from the given generate_pointcloud.py, but optimised because it was way too slow (around 50-100 times faster)
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

        return np.column_stack((X, Y, Z)), colors, depthMask

    # Does contain duplicates
    @staticmethod
    def getSamplePointsIndices(width, height, ratio):
        sampleNumber = int(ratio * width * height)

        sampledX = np.random.choice(
            np.arange(width), sampleNumber, replace=True)
        sampledY = np.random.choice(
            np.arange(height), sampleNumber, replace=True)

        return sampledX, sampledY
