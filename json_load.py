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
                data.append(keypoints)
            except:
                pass
    return data


if __name__ == "__main__": 
    #load json data from arg1 path
    directory = sys.argv[1]
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(load_json(directory))

    
