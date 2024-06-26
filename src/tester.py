import json_load as jl
import pprint
import metrics_lib
import sys
import stance_detector as sd
import os


# data = [frame1, frame2, ..., frame n]
# frame = {
#          knee:  x,y
#          wrist: x,y
#          ...
#          head:  x,y
#         }

if __name__ == "__main__":
    data = jl.load_json(sys.argv[1])
    if len(sys.argv) > 2:
        back_data = jl.load_json(sys.argv[2])
    frames = sd.stance_detector(data, False)
    chunks = sd.stance_detector(data, True)
    pp = pprint.PrettyPrinter(indent=4)

    print("Stances:")
    ids = []
    for frame in chunks:
        chunk = []
        for f in frame:
            chunk.append(f["ID"])
        ids.append(chunk)
    pp.pprint(ids)

    print("\nTorso lean:")
    pp.pprint(metrics_lib.torso_lean(frames, False))

    print("\nKnee flexion:")
    pp.pprint(metrics_lib.knee_flexion(data, False))

    print("\nTibia angle:")
    pp.pprint(metrics_lib.tibia_angle(data, False))

    print("\nFeet strike:")
    pp.pprint(metrics_lib.feet_strike(data, False))

    print("\nCenter of mass displacement:")
    pp.pprint(metrics_lib.CoM_displacement(data, False))

    print("\nElbow angle:")
    pp.pprint(metrics_lib.elbow_angle(frames, False))

    print("\nHip extension:")
    pp.pprint(metrics_lib.hip_extension(data, False))

    if len(sys.argv) > 2:
        print("\nPelvic drop:")
        pp.pprint(metrics_lib.pelvic_drop(back_data, False))
