import sys
import math


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
        dict: dictionary of frame ID and angle of torso lean
    """
    FILTER = 40 #angle filter to remove pose estimator errors
    MIN_REGULAR = 2 #minimal value of good torso lean
    MAX_REGULAR = 10 #maximum value of good torso lean
    degree_dict = {}
    for frame in data:
        radian_angle = math.atan2(frame["Neck"].y-frame["MidHip"].y, frame["Neck"].x-frame["MidHip"].x)
        torso_angle_degrees = math.degrees(radian_angle)+90
        if show_all and torso_angle_degrees < FILTER:
            degree_dict[frame["ID"]] = torso_angle_degrees
        elif torso_angle_degrees < FILTER and (torso_angle_degrees < MIN_REGULAR or torso_angle_degrees > MAX_REGULAR):
            degree_dict[frame["ID"]] = torso_angle_degrees
    
    return degree_dict




if __name__ == "__main__": 
    pass