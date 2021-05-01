import sys
import utils
import operator
import stance_detector as sd
import keypoint_class


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
            degree_dict[frame["ID"]] = -torso_angle

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
        dict: dictionary of frame IDs and corresponding CoM displacement angles compared to highest point in flight phase
    """
    FILTER = 80
    MAX_VAL = 5
    degree_dict = {}
    chunks = sd.stance_detector(data, True)
    right_direction = utils.is_going_right(data)

    tmp = chunks[0]
    for chunk in chunks[1:]:
        sublist = []
        #find indices
        for frame,i in zip(data,range(len(data))):
            if frame["ID"] == tmp[0]["ID"]:
                start = i
            if frame["ID"] == chunk[0]["ID"]:
                end = i
        #find highest point
        for frame in data[start:end]:
            sublist.append(frame["MidHip"].y)
        top = start + sublist.index(max(sublist))

        displacement_degree = abs(utils.angle_2points(tmp[0]["MidHip"], data[top]["MidHip"]))
        if right_direction:
            displacement_degree = 180 - displacement_degree
        if show_all:
            degree_dict[tmp[0]["ID"]] = displacement_degree
        elif displacement_degree < FILTER and displacement_degree > MAX_VAL:
            degree_dict[tmp[0]["ID"]] = displacement_degree

        tmp = chunk
    return degree_dict
        

def knee_flexion(data: list, show_all: bool) -> dict:
    """Calculate maximum angle of knee flexion during stance phase

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and knee flexion angles with maximum value for each stance phase
    """
    MIN_VAL = 40
    angle_dict = {}
    chunks = sd.stance_detector(data, True)
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
    stances = sd.stance_detector(data, False)
    angle_dict = {}
    for frame in stances:
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


def hip_extension(data: list, show_all: bool) -> dict:
    """Calculate hip extension angle at the end of stance phase

    Args:
        data (list): data structure of keypoint positions from pose estimator
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and hip extension angles
    """
    # biggest knee angle after stance -> stops growing
    chunks = sd.stance_detector(data, True)
    angle_dict = {}
    MIN_VAL = 10

    for chunk in chunks:
        post_chunk_id = chunk[0]["ID"] + 1
        list_pos = 0
        for frame in data:
            if frame["ID"] == post_chunk_id: # after stance
                break
            list_pos += 1

        tmp_angles = {}
        knee_dict = {}
        for pos in range(list_pos,list_pos+5): # 5 frames after stance
            try:
                frame = data[pos]
            except IndexError:
                continue
            if chunk[0]["StanceLeg"] == "Right":
                knee_angle = utils.angle_3points(frame["RAnkle"], frame["RKnee"], frame["RHip"])
                knee_dict[frame["ID"]] = knee_angle

                tmp_keypoint = keypoint_class.Keypoint(frame["RHip"].x, frame["RHip"].y-10, 1)
                angle = utils.angle_3points(frame["RKnee"], frame["RHip"], tmp_keypoint)
            else:
                knee_angle = utils.angle_3points(frame["LAnkle"], frame["LKnee"], frame["LHip"])
                knee_dict[frame["ID"]] = knee_angle

                tmp_keypoint = keypoint_class.Keypoint(frame["LHip"].x, frame["LHip"].y-10, 1)
                angle = utils.angle_3points(frame["LKnee"], frame["LHip"], tmp_keypoint)
            angle = 180 - angle
            tmp_angles[frame["ID"]] = angle

        max_angle_id = max(knee_dict.items(), key=operator.itemgetter(1))[0]
        if show_all:
            angle_dict[max_angle_id] = tmp_angles[max_angle_id]
        elif tmp_angles[max_angle_id] < MIN_VAL:
            angle_dict[max_angle_id] = tmp_angles[max_angle_id]
    return angle_dict


def pelvic_drop(data: list, show_all: bool) -> dict:
    """Calculate angle of pelvic drop from back view

    Args:
        data (list): data structure of keypoint positions from pose estimator - back view
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and pelvic drop angles
    """
    FILTER = 80
    MAX_ANGLE = 6
    angle_dict = {}
    for frame in data[0:40]:
        angle = utils.angle_2points(frame["RHip"], frame["LHip"])
        angle = abs(angle)
        if show_all and angle < FILTER:
            angle_dict[frame["ID"]] = angle
        elif angle > MAX_ANGLE and angle < FILTER:
            angle_dict[frame["ID"]] = angle
    
    return angle_dict


def parallel_legs(data: list, show_all: bool) -> dict:
    """Determine if thighs are parallel from back view

    Args:
        data (list): data structure of keypoint positions from pose estimator - back view
        show_all (bool): whether to return values for each stance or only irregular ones

    Returns:
        dict: dictionary of frame IDs and angles between legs
    """
    angle_dict = {}
    for frame in data[10:30]:
        angle_R = utils.angle_2points(frame["RKnee"], frame["RHip"])
        angle_L = utils.angle_2points(frame["LKnee"], frame["LHip"])
        diff = abs(angle_R - angle_L)
        if show_all:
            angle_dict[frame["ID"]] = diff
        elif diff > 10:
            angle_dict[frame["ID"]] = diff
    
    return angle_dict


if __name__ == "__main__":
    pass
