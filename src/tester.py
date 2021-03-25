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
    frames = sd.stance_detector(data, False)
    #torso = metrics_lib.torso_lean(data, False)
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(torso)

    print("Stances:")
    ids = []
    for frame in frames:
        ids.append(frame["ID"])
    pp.pprint(ids)

    print("Torso lean:")
    pp.pprint(metrics_lib.torso_lean(frames, False))

    print("Knee flexion:")
    pp.pprint(metrics_lib.knee_flexion(data, False))

    print("Tibia angle:")
    pp.pprint(metrics_lib.tibia_angle(data, False))

    print("Center of mass displacement:")
    pp.pprint(metrics_lib.CoM_displacement(data, False))

    print("Elbow angle:")
    pp.pprint(metrics_lib.elbow_angle(frames, False))

    print("Hip extension:")
    pp.pprint(metrics_lib.hip_extension(data, False))
