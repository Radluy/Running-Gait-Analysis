import utils


# [[1,2,3], [6,7,8], [15,16]...]
def create_frame_chunks(frame_list: list) -> list:
    """Merges concurrent frames into chunks

    Args:
        frame_list (list): list of frames to be merged

    Returns:
        list: list of chunks, one chunk is array of frames
    """
    tmp_frame = frame_list[0]
    chunk_list = [[tmp_frame]]

    # merge into list if they're concurrent
    for frame in frame_list[1:]:
        if frame["ID"] == tmp_frame["ID"]+1:
            chunk_list[-1].append(frame)
        else:
            chunk_list.append([frame])
        tmp_frame = frame

    return chunk_list


def stance_detector(data: list, merge_to_chunks: bool) -> list:
    """Finds frames with runner in a stance phase

    Args:
        list (data): data structure of keypoint positions from pose estimator

    Returns:
        list: array of frames with stance phase detected
    """
    FOOT_EPSILON = 10  # max possible angle
    TIBIA_EPSILON = 25  # max possible angle
    frame_list = []
    keypoints = ["RBigToe", "RHeel", "LBigToe",
                 "LHeel", "RKnee", "RAnkle", "LKnee", "LAnkle"]

    for frame in data:
        for keypoint in keypoints:  # skip if needed keypoints not in the frame
            if frame[keypoint].confidence == 0:
                break
        else:
            # add to results if angles are within limit
            foot_R_angle = abs(utils.angle_2points(
                frame["RBigToe"], frame["RHeel"]))
            foot_L_angle = abs(utils.angle_2points(
                frame["LBigToe"], frame["LHeel"]))
            tibia_R_angle = abs(utils.angle_2points(
                frame["RKnee"], frame["RAnkle"]))
            tibia_L_angle = abs(utils.angle_2points(
                frame["LKnee"], frame["LAnkle"]))
            if (foot_R_angle < FOOT_EPSILON or foot_R_angle > 180 - FOOT_EPSILON) and (tibia_L_angle < TIBIA_EPSILON or tibia_L_angle > 180 - TIBIA_EPSILON):
                frame["StanceLeg"] = "Right"
                frame_list.append(frame)
            if (foot_L_angle < FOOT_EPSILON or foot_L_angle > 180 - FOOT_EPSILON) and (tibia_R_angle < TIBIA_EPSILON or tibia_R_angle > 180 - TIBIA_EPSILON):
                frame["StanceLeg"] = "Left"
                frame_list.append(frame)

    if merge_to_chunks:
        chunks = create_frame_chunks(frame_list)
        return chunks

    return frame_list
