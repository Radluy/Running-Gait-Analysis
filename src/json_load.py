import json
import sys
import os
import pprint
from keypoint_class import Keypoint

# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }

# order of keypoints specified in OpenPose documentation
keypoint_order = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
                  "LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip",
                  "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe",
                  "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel", "Background"]


def load_json(json_directory_path: str) -> list:
    """load json files from a directory and return as an array of dictionaries

    Args:
        json_directory_path (str): path to directory containing json files

    Returns:
        list: list of dictionaries representing individual frames
    """
    data = []
    files = os.listdir(json_directory_path)
    counter = -1
    for file in files:
        counter += 1
        path = os.path.join(json_directory_path, file)
        with open(path) as json_file:
            json_struct = json.load(json_file)
            try:
                keypoints = json_struct["people"][0]["pose_keypoints_2d"]
            except:  # skip empty frames
                continue
            keypoint_dict = {}
            keypoint_dict["ID"] = counter
            iterator = iter(keypoints)
            i = 0
            for x in iterator:  # iterate 3 at a time (x,y,conf)
                y = next(iterator)
                confidence = next(iterator)
                keypoint = Keypoint(x, y, confidence)
                keypoint_dict[keypoint_order[i]] = keypoint
                i += 1
            data.append(keypoint_dict)
    return data


if __name__ == "__main__":
    # load json data from arg1 path
    directory = sys.argv[1]
    pp = pprint.PrettyPrinter(indent=4)
    data = load_json(directory)

    pp.pprint(data)
