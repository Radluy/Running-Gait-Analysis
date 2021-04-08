import sys 
import filetype
import os
from folderClass import folderStruct
import metrics_lib
import stance_detector as sd


def check_formal_reqs(path: str) -> bool:
    json_exists = False
    images_exist = False
    video_exists = False

    if not os.path.isdir(path):
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
        return False
    else:
        return True


def load_folder_struct(path):
    correct_struct = check_formal_reqs(path)
    if not correct_struct:
        return None
    struct = folderStruct(path)
    return struct


# return new directory destination
def call_estimator(path_to_video):
    pass


def evaluate(side_data, back_data):
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
    except:
        pass

    return metric_values


def backend_setup(path1):
    isVideo = False
    if os.path.isdir(path1):
        return load_folder_struct(path1)
    try:
        kind = filetype.guess(path1)
    except:
        #TODO: INCORRECT PATH
        return
    if kind.mime[0:5] == "video":
        new_path = call_estimator(path1)
        return load_folder_struct(new_path)