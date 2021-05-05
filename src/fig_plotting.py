import json_load as jl
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict


def plot_stats():
    """Plot results of Openpose estimator accuracy testing 
    """

    # same index in 2 corresponding lists represents one point
    actual_x = [1172, 1175, 1260, 940, 1045, 880, 420, 391, 506]
    actual_y = [740, 860, 518, 738, 794, 525, 765, 884, 532]
    estimate_x = [1171, 1169, 1260, 945, 1048, 889, 424, 388, 506]
    estimate_y = [733, 862, 527, 733, 795, 530, 756, 892, 533]

    fig, ax = plt.subplots()
    ax.plot(actual_x, actual_y, 'go', alpha=0.4, label='Actual joint position')
    ax.plot(estimate_x, estimate_y, 'go', color='blue',
            alpha=0.4, label='Estimated joint position')

    ax.set_title('Actual and estimated X and Y coordinates')
    ax.legend()

    ax.grid()
    fig.tight_layout()
    plt.show()
    fig.savefig('./accuracy_testing.png')


def print_coords(ident: int):
    """prints coordinates of knee, ankle, and elbow of a single frame

    Args:
        ident (int): ID of frame to be printed 
    """
    data = jl.load_json(sys.argv[1])
    for frame in data:
        if frame["ID"] == ident:
            print("LKnee: {knee}\nLAnkle: {ankle}\nLElbow: {elbow}".format(
                knee=frame["LKnee"], ankle=frame["LAnkle"], elbow=frame["LElbow"]))


# stance frames merged into chunks for each video from dataset
data = [[[13], [21], [31, 32, 33], [42], [52, 53, 54, 55]],
        [[40], [42, 43, 44], [52], [59], [61, 62, 63], [71], [78], [81]],
        [[17, 18], [28], [39, 40], [49, 50, 51]],
        [],
        [[26], [35, 36, 37, 38], [46, 47], [56, 57, 58]],
        [[11, 12], [20, 21, 22, 23], [29], [31]],
        [[29], [39, 40], [49, 50], [60, 61], [71]],
        [[27, 28], [38, 39], [49, 50, 51], [62]],
        [[30, 31, 32], [41, 42], [50, 51, 52]],
        [[19, 20], [30], [41], [50, 51, 52]]]

names = ['vid0', 'vid1', 'vid2', 'vid3', 'vid4',
         'vid5', 'vid6', 'vid7', 'vid8', 'vid9']


def plot_stances_num():
    """Plot number of stance phases on the dataset
    """

    lengths = []
    for a in data:
        lengths.append(len(a))

    fig, ax = plt.subplots()
    ax.bar(range(10), lengths, color='orange')
    plt.xticks(np.arange(0, 10, 1), names)

    ax.set_title('Number of stance phases detected')

    fig.tight_layout()
    plt.show()
    fig.savefig('./stance_num.png')


def plot_frames_per_stance():
    """Plot number of frames per single stance phase in the dataset
    """

    lengths = []
    for vid in data:
        for chunk in vid:
            lengths.append(len(chunk))

    # traverse lists by lengths
    res = [(el, lengths.count(el)) for el in lengths]
    fin = list(OrderedDict(res).items())

    nms = []
    vals = []
    for tup in fin:
        nms.append(str(tup[0])+' frame/s')
        vals.append(tup[1])

    fig, ax = plt.subplots()
    ax.pie(vals, labels=nms, autopct='%1.2f%%')
    ax.set_title('Number of frames per one stance phase')

    fig.tight_layout()
    plt.show()
    fig.savefig('./frames_per_stance.png')


def plot_stance_dist():
    """Plot distances between stance phases on the dataset
    """

    distances = []
    # distance between first frames of chunks
    for vid in data:
        for i in range(len(vid)-1):
            dist = vid[i+1][0] - vid[i][0]
            distances.append(dist)

    fig, ax = plt.subplots()
    ax.hist(distances, edgecolor='black', linewidth=1.2)
    plt.xticks(np.arange(0, 13, 1))
    ax.set_title('Distance between beginnings of stance phases in frames')
    plt.xlabel('Frames')
    plt.ylabel('Occurences')

    fig.tight_layout()
    plt.show()
    fig.savefig('./stance_dist.png')


if __name__ == "__main__":
    plot_stats()
    plot_stances_num()
    plot_frames_per_stance()
    plot_stance_dist()
