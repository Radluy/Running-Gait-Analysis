import json_load  as jl
import pprint
import metrics_lib
import sys

# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }


if __name__ == "__main__": 
    data = jl.load_json(sys.argv[1])
    #frames = metrics_lib.elbow_angle(data, False)
    frames = metrics_lib.stance_detector(data)
    #elbows = metrics_lib.elbow_angle(frames, True)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(frames)
    #pp.pprint(elbows)
