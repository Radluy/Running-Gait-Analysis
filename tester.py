import json_load  as jl
import sys


# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }

epsilon = 20

data = jl.load_json(sys.argv[1])
for frame in data:
    difference = abs(frame["RHeel"].y - frame["RBigToe"].y) 
    if difference < epsilon and frame["RHeel"].confidence != 0 and frame["RBigToe"].confidence != 0:
        print(frame["ID"])
