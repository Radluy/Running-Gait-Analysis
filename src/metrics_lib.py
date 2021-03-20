import sys
import utils
import operator
import stance_detector as sd


# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }


def torso_lean(data: list, show_all: bool) -> dict:
    """calculate torso lean angle for each frame

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each frame or only irregular ones

    Returns:
        dict: dictionary of frame IDs and angles of torso lean
    """
    FILTER = 40  # angle filter to remove pose estimator errors
    MIN_REGULAR = 2  # minimal value of good torso lean
    MAX_REGULAR = 10  # maximum value of good torso lean
    degree_dict = {}
    right_direction = utils.is_going_right(data)
    for frame in data:
        torso_angle = utils.angle_2points(
            frame["Neck"], frame["MidHip"])+90
        if show_all:
            degree_dict[frame["ID"]] = torso_angle
        elif right_direction and torso_angle < FILTER and (torso_angle < MIN_REGULAR or torso_angle > MAX_REGULAR):
            degree_dict[frame["ID"]] = torso_angle
        elif (not right_direction) and torso_angle < FILTER and (torso_angle > -MIN_REGULAR or torso_angle < -MAX_REGULAR):
            degree_dict[frame["ID"]] = torso_angle

    return degree_dict


def elbow_angle(data: list, show_all: bool) -> dict:
    """calculate elbow angle in every frame

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each frame or only irregular ones

    Returns:
        dict: dictionary of frame IDs and elbow angles
    """
    CORRECT_VAL = 90
    EPSILON = 30
    degree_dict = {}
    right_direction = utils.is_going_right(data)
    for frame in data:
        if right_direction:
            elbow_angle = utils.angle_3points(
                frame["RWrist"], frame["RElbow"], frame["RShoulder"])
        else:
            elbow_angle = utils.angle_3points(
                frame["LWrist"], frame["LElbow"], frame["LShoulder"])
        if show_all:
            degree_dict[frame["ID"]] = elbow_angle
        elif elbow_angle > CORRECT_VAL + EPSILON or elbow_angle < CORRECT_VAL - EPSILON:
            degree_dict[frame["ID"]] = elbow_angle
    return degree_dict


def CoM_displacement(data: list, show_all: bool) -> dict:
    """Calculate angle of vertical Center of Mass displacement

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each frame or only irregular ones

    Returns:
        dict: dictionary of frame IDs and corresponding CoM displacement angles compared to previous frame
    """
    FILTER = 80
    MAX_VAL = 20
    tmp_frame = data[0]
    degree_dict = {}
    right_direction = utils.is_going_right(data)
    for frame in data[1:]:
        displacement_degree = abs(utils.angle_2points(
            tmp_frame["MidHip"], frame["MidHip"]))
        if right_direction:
            displacement_degree = 180 - displacement_degree
        if show_all:
            degree_dict[frame["ID"]] = displacement_degree
        elif displacement_degree < FILTER and displacement_degree > 20:
            degree_dict[frame["ID"]] = displacement_degree
        tmp_frame = frame
    return degree_dict


def knee_flexion(chunks: list, show_all: bool) -> dict:
    """Calculate maximum angle of knee flexion during stance phase

    Args:
        chunks (list): list of chunks with individual stances from stance detector
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and knee flexion angles with maximum value for each stance phase
    """
    MIN_VAL = 40
    angle_dict = {}
    for chunk in chunks:
        angles = {}
        for frame in chunk:
            if frame["StanceLeg"] == "Right":
                angle = 180 - \
                    utils.angle_3points(
                        frame["RHip"], frame["RKnee"], frame["RAnkle"])
            else:
                angle = 180 - \
                    utils.angle_3points(
                        frame["LHip"], frame["LKnee"], frame["LAnkle"])
            # print("{id}: {angle}".format(id=frame["ID"], angle=angle)) # debug
            angles[frame["ID"]] = angle
        max_angle_id = max(angles.items(), key=operator.itemgetter(1))[0]
        if show_all:
            angle_dict[max_angle_id] = angles[max_angle_id]
        elif angles[max_angle_id] < MIN_VAL:
            angle_dict[max_angle_id] = angles[max_angle_id]
    return angle_dict


def tibia_angle(data: list, show_all: bool) -> dict:
    """Calculate angle of stance leg tibia during stance phase

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and stance leg tibia angles 
    """
    right_direction = utils.is_going_right(data)
    # chunks = sd.create_frame_chunks(data)
    angle_dict = {}
    for frame in data:
        if right_direction:
            if frame["StanceLeg"] == "Right":
                angle = utils.angle_2points(frame["RAnkle"], frame["RKnee"])
            else:
                angle = utils.angle_2points(frame["LAnkle"], frame["LKnee"])
        else:
            if frame["StanceLeg"] == "Right":
                angle = utils.angle_2points(frame["RAnkle"], frame["RKnee"])
            else:
                angle = utils.angle_2points(frame["LAnkle"], frame["LKnee"])
        if show_all:
            angle_dict[frame["ID"]] = angle
        elif right_direction and angle < 90:
            angle_dict[frame["ID"]] = angle
        elif not right_direction and angle > 90:
            angle_dict[frame["ID"]] = angle
    return angle_dict


def feet_strike(data: list, show_all: bool) -> dict:
    """Calculate feet strike angle

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and feet strike angles
    """
    MAX_ANGLE = 20
    chunks = sd.stance_detector(data, True)
    right_direction = utils.is_going_right(data)
    angle_dict = {}
    for chunk in chunks:
        pre_chunk_id = chunk[0]["ID"] - 1
        pre_frame = None
        for frame in data:
            if frame["ID"] == pre_chunk_id:
                pre_frame = frame
                break
        if chunk[0]["StanceLeg"] == "Right":
            angle = abs(utils.angle_2points(pre_frame["RBigToe"], pre_frame["RHeel"]))
        else:
            angle = abs(utils.angle_2points(pre_frame["LBigToe"], pre_frame["LHeel"]))
        if not right_direction:
            angle = 180 - angle
        if show_all:
            angle_dict[pre_chunk_id] = angle
        elif angle > MAX_ANGLE:
            angle_dict[pre_chunk_id] = angle
    return angle_dict


if __name__ == "__main__":
    pass
