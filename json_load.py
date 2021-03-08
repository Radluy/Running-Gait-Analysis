import json
import sys
import os
import pprint

# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }
#data = []

keypoint_order = ["Nose","Neck","RShoulder","RElbow","RWrist","LShoulder",
                  "LElbow","LWrist","MidHip","RHip","RKnee","RAnkle","LHip",
                  "LKnee","LAnkle","REye","LEye","REar","LEar","LBigToe",
                  "LSmallToe","LHeel","RBigToe","RSmallToe", "RHeel", "Background"]

class Keypoint():
    def __init__(self, x, y, confidence):
        self.x = x
        self.y = y
        self.confidence = confidence 


def load_json(json_directory_path: str): 
    """ load json files from a directory and return as an array of dictionaries"""
    data = []
    files = os.listdir(json_directory_path)
    for file in files:
        path = os.path.join(json_directory_path, file)
        with open(path) as json_file:
            json_struct = json.load(json_file)
            try:
                keypoints = json_struct["people"][0]["pose_keypoints_2d"]
                keypoint_dict = {}
                iterator = iter(keypoints)
                i = 0
                for x in iterator:
                    y = next(iterator)
                    confidence = next(iterator)
                    keypoint = Keypoint(x, y, confidence)
                    keypoint_dict[keypoint_order[i]] = keypoint
                    i += 1
                data.append(keypoint_dict)
            except:
                # TODO: log error
                pass
    return data


if __name__ == "__main__": 
    # load json data from arg1 path
    directory = sys.argv[1]
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(load_json(directory))

    
