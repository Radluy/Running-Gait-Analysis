from keypoint_class import Keypoint
import json_load as jl
import sys
import os
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps


def plot_keypoint_trajectory(data: list, joint: str, image_path: str, save_path: str):
    """plot trajectory of one keypoint from pose estimator

    Args:
        data (list): data structure from pose estimator
        joint (str): name of the studied keypoint
        image_path (str): path to one image from pose estimator used to determine dimensions
    """
    my_dpi = 96
    image = Image.open(image_path)
    width, height = image.size

    x_dims = []
    y_dims = []
    for frame in data:
        try:
            keypoint = frame[joint]
        except KeyError:
            print("Incorrect keypoint name")
            return

        if keypoint.confidence != 0:
            x_dims.append(keypoint.x)
            y_dims.append(height - keypoint.y)

    fig = plt.figure(figsize=(640/my_dpi, 360/my_dpi), dpi=my_dpi)
    plt.plot(x_dims, y_dims)
    plt.xlim(left=0, right=width)
    plt.ylim(bottom=0, top=height)
    plt.axis('off')

    # print image as background
    #image = ImageOps.flip(image)
    #plt.imshow(image)

    #plt.show()
    fig.tight_layout()
    fig.savefig(os.path.join(save_path,'{}_trajectory.png'.format(joint)), transparent=True)


if __name__ == "__main__":
    data = jl.load_json(sys.argv[1])
    plot_keypoint_trajectory(data, "RKnee", sys.argv[2])
