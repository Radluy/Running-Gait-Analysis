from pymediainfo import MediaInfo
import sys 
import filetype
import os
from folderClass import folderStruct
import pprint


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
        return
    struct = folderStruct(path)
    return struct


# return new directory destination
def call_estimator(path_to_video):
    pass


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
        print("ISVIDEO")
        new_path = call_estimator(path1)
        return load_folder_struct(new_path)