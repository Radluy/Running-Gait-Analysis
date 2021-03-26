from keypoint_class import Keypoint
import json_load as jl
import sys
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps


def create_keypoint_trajectory(data: list, joint: str, image_path: str):

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

    fig = plt.figure(figsize=(6, 3), dpi=150)
    plt.plot(x_dims, y_dims)
    plt.xlim(left=0, right=width)
    plt.ylim(bottom=0, top=height)

    # print image as background
    image = ImageOps.flip(image)
    plt.imshow(image)

    plt.show()
    fig.tight_layout()
    # fig.savefig('{}_trajectory.png'.format(joint), dpi=200) 


if __name__ == "__main__":
    data = jl.load_json(sys.argv[1])
    create_keypoint_trajectory(data, "RKnee", sys.argv[2])
