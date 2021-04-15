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
    back_data = jl.load_json(sys.argv[2])
    frames = sd.stance_detector(data, False)
    pp = pprint.PrettyPrinter(indent=4)

    print("Stances:")
    ids = []
    for frame in frames:
        ids.append(frame["ID"])
    pp.pprint(ids)

    print("\nTorso lean:")
    pp.pprint(metrics_lib.torso_lean(frames, False))

    print("\nKnee flexion:")
    pp.pprint(metrics_lib.knee_flexion(data, False))

    print("\nTibia angle:")
    pp.pprint(metrics_lib.tibia_angle(data, False))

    print("\nCenter of mass displacement:")
    pp.pprint(metrics_lib.CoM_displacement(data, False))

    print("\nElbow angle:")
    pp.pprint(metrics_lib.elbow_angle(frames, False))

    print("\nHip extension:")
    pp.pprint(metrics_lib.hip_extension(data, False))

    print("\nPelvic drop:")
    pp.pprint(metrics_lib.pelvic_drop(back_data, False))

    #print("\nHeel whips:")
    #pp.pprint(metrics_lib.heel_whips(back_data, False))

    print("\nParallel legs:")
    pp.pprint(metrics_lib.parallel_legs(back_data, False))
