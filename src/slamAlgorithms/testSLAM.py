from src.slamAlgorithms.baseSLAM import BaseSLAM
import numpy as np
from src.camera import CameraLocations
from pyquaternion import Quaternion
from copy import deepcopy
from scipy.spatial.transform import Rotation as R


# Generate some randomized translations and rotations in order to showcase the metrics
class TestSLAM(BaseSLAM):

    def __init__(self, data):
        self.data = data

    def extractCameraMovement(self):
        firstTimeStamp = self.data.timestamps[0]
        self.data.modeledCamLocs[firstTimeStamp] = self.data.trueCamLocs[firstTimeStamp]
        
        randomTrans = np.random.sample(3) / 100
        randomquat = np.random.sample(4)

        for index, timeStamp in enumerate(self.data.timestamps[:-1]):

            nextTimeStamp = self.data.timestamps[index + 1]

            location = self.data.trueCamLocs[timeStamp]
            modelLocation = deepcopy(location)

            # Add randomisation to translation
            modelLocation.translation += np.log(index + 2) * randomTrans

            # Add randomisation to translation
            r = R.from_quat(np.sqrt(index + 1) * randomquat)
            quat = Quaternion(matrix=r.as_matrix())

            modelLocation.quaternion = quat * location.quaternion
            self.data.modeledCamLocs[nextTimeStamp] = modelLocation

        return self.data
