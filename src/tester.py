import json_load as jl
import pprint
import metrics_lib
import sys
import stance_detector as sd


# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }


if __name__ == "__main__":
    data = jl.load_json(sys.argv[1])
    frames = sd.stance_detector(data, True)
    elbows = metrics_lib.knee_flexion(frames, False)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(elbows)
