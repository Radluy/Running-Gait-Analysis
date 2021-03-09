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
    
    def __repr__(self):
        return ("""x: {x}, y: {y}, confidence: {conf}""".format(x=self.x, y=self.y, conf=self.confidence))


def load_json(json_directory_path: str) -> list: 
    """ load json files from a directory and return as an array of dictionaries"""
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
            except:
                # TODO: log error
                print("empty frame!", file=sys.stderr)
                continue
            keypoint_dict = {}
            keypoint_dict["ID"] = counter
            iterator = iter(keypoints)
            i = 0
            for x in iterator:
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
    


    
