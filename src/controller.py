import sys 
import filetype
import os
from folderClass import folderStruct
import metrics_lib
import stance_detector as sd
from estimator import estimate
import sync


def check_formal_reqs(path: str) -> bool:
    """Checks formal requirements for directory like existance of necessary files

    Args:
        path (str): path to directory

    Returns:
        bool: True if the directory structure is valid, False otherwise
    """
    json_exists = False
    images_exist = False
    video_exists = False

    if not os.path.isdir(path):
        print("log: Input path is not a directory!", file=sys.stderr)
        return False
    
    files = os.listdir(path)
    for file in files:
        if file == "images":
            images_exist = True
        elif file == "json":
            json_exists = True
        elif file == "video_est.avi":
            video_exists = True
    
    if not json_exists or not images_exist or not video_exists:
        print("log: Missing data in directory!", file=sys.stderr)
        return False
    else:
        return True


def load_folder_struct(path: str) -> folderStruct:
    """Load directory into folderStruct class instance

    Args:
        path (str): path to directory

    Returns:
        folderStruct: instance of folderStruct or None if incorrect path is specified
    """
    correct_struct = check_formal_reqs(path)
    if not correct_struct:
        print("log: Incorrect structure of directory!", file=sys.stderr)
        return None
    struct = folderStruct(path)
    return struct


def evaluate(side_data: folderStruct, back_data: folderStruct) -> dict:
    """Apply metrics computations

    Args:
        side_data (folderStruct): data from side camera
        back_data (folderStruct): data from posterior camera

    Returns:
        dict: dictionary where keys are metric names and 
        values are dictionaries from corresponding metrics library methods 
    """
    frames = sd.stance_detector(side_data, False)
    metric_values = {}
    ids = []
    for frame in frames:
        ids.append(frame["ID"])
    metric_values["Stances"] = ids

    try:
        metric_values["Torso Lean"] = metrics_lib.torso_lean(frames, False)
        metric_values["Knee Flexion"] = metrics_lib.knee_flexion(side_data, False)
        metric_values["Tibia Angle"] = metrics_lib.tibia_angle(side_data, False)
        metric_values["Center of Mass Displacement"] = metrics_lib.CoM_displacement(side_data, False)
        metric_values["Elbow Angle"] = metrics_lib.elbow_angle(frames, False)
        metric_values["Hip Extension"] = metrics_lib.hip_extension(side_data, False)
        metric_values["Feet Strike"] = metrics_lib.feet_strike(side_data, False)
        metric_values["Pelvic Drop"] = metrics_lib.pelvic_drop(back_data, False)
        metric_values["Parallel Legs"] = metrics_lib.parallel_legs(back_data, False)
    except:
        pass

    return metric_values


def backend_setup(path1: str) -> folderStruct:
    """Setup folderStruct instance for input video or directory

    Args:
        path1 (str): path to either video or directory

    Returns:
        folderStruct: folderStruct instance with loaded data corresponding to input
        or None if path is not valid
    """
    if os.path.isdir(path1):
        return load_folder_struct(path1)
    try:
        kind = filetype.guess(path1)
    except:
        print("log: File is not a video!", file=sys.stderr)
        return None
    if kind.mime[0:5] == "video":
        new_path = estimate(path1)
        return load_folder_struct(new_path)
    else:
        return None


def auto_sync(side_data: folderStruct, back_data: folderStruct):
    chunks = sd.stance_detector(side_data, True)
    if chunks[0][0]["StanceLeg"] == "Right":
        leg = "L"
    else:
        leg = "R"

    side_frame = sync.find_side_sync_point(side_data)
    back_frame = sync.find_back_sync_point(back_data, leg)

    id_dict = {}
    id_dict["side"] = int(side_frame)
    id_dict["back"] = int(back_frame)

    return id_dict