import math
import numpy as np
from keypoint_class import Keypoint


def angle_2points(k1: Keypoint, k2: Keypoint) -> float:
    """calculate angle between 2 points in 2 dimensions

    Args:
        k1 (Keypoint): first instance of keypoint class
        k2 (Keypoint): second instance of keypoint class

    Returns:
        float: the angle between two keypoints
    """
    radian_angle = math.atan2(k1.y-k2.y, k1.x-k2.x)
    degrees_angle = math.degrees(radian_angle)
    return degrees_angle


def angle_3points(k1: Keypoint, k2: Keypoint, k3: Keypoint) -> float:
    """calculate angle between 3 points in 2 dimensions

    Args:
        k1 (Keypoint): first instance of keypoint class
        k2 (Keypoint): second instance of keypoint class
        k3 (Keypoint): third instance of keypoint class

    Returns:
        float: the angle between three keypoints
    """
    # https://stackoverflow.com/questions/35176451/python-code-to-calculate-angle-between-three-point-using-their-3d-coordinates
    a = np.array([k1.x, k1.y])
    b = np.array([k2.x, k2.y])
    c = np.array([k3.x, k3.y])
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    radian_angle = np.arccos(cosine_angle)
    return np.degrees(radian_angle)
