import json_load as jl
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_stats():

    actual_x = [1172, 1175, 1260, 940, 1045, 880, 420, 391, 506]
    actual_y = [740, 860, 518, 738, 794, 525, 765, 884, 532]
    estimate_x = [1171, 1169, 1260, 945, 1048, 889, 424, 388, 506]
    estimate_y = [733, 862, 527, 733, 795, 530, 756, 892, 533]

    fig, ax = plt.subplots()
    ax.plot(actual_x, actual_y, 'go', alpha=0.4, label='Actual joint position')
    ax.plot(estimate_x, estimate_y, 'go', color='blue', alpha=0.4, label='Estimated joint position')

    ax.set_title('Actual and estimated X and Y coordinates')
    ax.legend()

    ax.grid()
    fig.tight_layout()
    plt.show()
    fig.savefig('./accuracy_testing.png')


def print_coords():
    data = jl.load_json(sys.argv[1])
    for frame in data:
        if frame["ID"] == 60:
            print("LKnee: {knee}\nLAnkle: {ankle}\nLElbow: {elbow}".format(knee=frame["LKnee"], ankle=frame["LAnkle"], elbow=frame["LElbow"]))



if __name__ == "__main__":
    plot_stats()

    