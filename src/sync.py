import json_load as jl
import sys
import utils
import stance_detector as sd


def right_leg_front(frame: dict) -> bool:
    """determine which leg is in the front 

    Args:
        frame (dict): one frame from pose estimator

    Returns:
        bool: True if right leg is in the front, False otherwise
    """
    if frame["RKnee"].x > frame["LKnee"].x:
        return True
    else:
        return False


def find_side_sync_point(side_data: list) -> int:
    """finds synchronization frame from side view.
    frame from stance chunk with smallest knee angle of back leg

    Args:
        side_data (list): data structure from pose estimator

    Returns:    
        [int]: ID of sync frame
    """
    chunks = sd.stance_detector(side_data, True)

    chunk = chunks[0]
    min_angle = 180
    min_id = None
    for frame in chunk:
        if frame["StanceLeg"] == "Right":
            angle = utils.angle_3points(
                    frame["LAnkle"], frame["LKnee"], frame["LHip"])
        else:
            angle = utils.angle_3points(
                    frame["RAnkle"], frame["RKnee"], frame["RHip"])
        if angle < min_angle:
            min_angle = angle
            min_id = frame["ID"]

    return min_id


def find_back_sync_point(back_data: list, leg: str)-> int:
    """find synchronization frame from back view
    frame with ankle highest above knee of the back leg

    Args:
        back_data (list): data structure from pose estimator
        leg (str): R/L string, determines which leg is back one

    Returns:
        int: ID of sync frame
    """
    distance = back_data[0][leg+"Knee"].y - back_data[0][leg+"Ankle"].y
    current_id = back_data[0]["ID"]
    for frame in back_data[1:]:
        # check for incomplete frames
        if frame[leg+"Knee"].y == 0 or frame[leg+"Ankle"].y == 0:
            continue

        new_distance = frame[leg+"Knee"].y - frame[leg+"Ankle"].y
        if new_distance > distance:
            return current_id
        else:
            distance = new_distance
            current_id = frame["ID"]

    return current_id

if __name__ == "__main__":
    side_data = jl.load_json(sys.argv[1])
    back_data = jl.load_json(sys.argv[2])

    chunks = sd.stance_detector(side_data, True)
    if chunks[0][0]["StanceLeg"] == "Right":
        leg = "L"
    else:
        leg = "R"

    print("side frame: {}".format(find_side_sync_point(side_data)))
    print("back frame: {}".format(find_back_sync_point(back_data, leg)))