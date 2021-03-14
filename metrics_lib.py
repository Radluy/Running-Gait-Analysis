import sys
import utils

# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }

def find_stance_phases(data: list) -> list:
    """Find frames with runner in a stance phase

    Args:
        list (data): data structure of keypoint positions from pose estimator

    Returns:
        list: array of frame IDs where stance phase was detected
    """
    # 30-20-10-15 tested
    EPSILON = 20
    frame_list = []

    for frame in data:
        R_difference = abs(frame["RHeel"].y - frame["RBigToe"].y) 
        L_difference = abs(frame["LHeel"].y - frame["LBigToe"].y) 
        if R_difference < EPSILON and frame["RHeel"].confidence != 0 and frame["RBigToe"].confidence != 0:
            frame_list.append(frame["ID"])
        if L_difference < EPSILON and frame["LHeel"].confidence != 0 and frame["LBigToe"].confidence != 0:
            frame_list.append(frame["ID"])   

    return frame_list
    
def torso_lean(data: list, show_all: bool) -> dict:
    """calculate torso lean angle for each frame

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each frame or only irregular ones

    Returns:
        dict: dictionary of frame IDs and angles of torso lean
    """
    FILTER = 40 # angle filter to remove pose estimator errors
    MIN_REGULAR = 2 # minimal value of good torso lean
    MAX_REGULAR = 10 # maximum value of good torso lean
    degree_dict = {}
    for frame in data:
        torso_angle = utils.angle_2points(frame["Neck"], frame["MidHip"])
        if show_all and torso_angle < FILTER:
            degree_dict[frame["ID"]] = torso_angle
        elif torso_angle < FILTER and (torso_angle < MIN_REGULAR or torso_angle > MAX_REGULAR):
            degree_dict[frame["ID"]] = torso_angle
    
    return degree_dict

def elbow_angle(data: list, show_all: bool) -> list:
    """calculate elbow angle in every frame

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each frame or only irregular ones

    Returns:
        list: dictionary of frame IDs and elbow angles
    """
    CORRECT_VAL = 90 #
    EPSILON = 30
    degree_dict = {}
    for frame in data:
        elbow_angle = utils.angle_3points(frame["RWrist"], frame["RElbow"], frame["RShoulder"])
        if show_all:
            degree_dict[frame["ID"]] = elbow_angle
        elif elbow_angle > CORRECT_VAL + EPSILON or elbow_angle < CORRECT_VAL - EPSILON:
            degree_dict[frame["ID"]] = elbow_angle
    return degree_dict



if __name__ == "__main__": 
    pass