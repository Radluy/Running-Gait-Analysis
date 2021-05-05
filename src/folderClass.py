import os
import json_load as jl
from trajectory import plot_keypoint_trajectory

# keypoints for trajectories
keypoints = ["RKnee", "LKnee", "LAnkle", "RAnkle", "Neck", "MidHip"]

# keypoint name mapping for UI
keypoint_map = {
    "RKnee": "Right Knee",
    "LKnee": "Left Knee",
    "Neck": "Neck",
    "MidHip": "Middle of hips",
    "RAnkle": "Right Ankle",
    "LAnkle": "Left Ankle",
}


class folderStruct():
    """Class that holds images, coordinate data structure, rendered video, trajectories and metric values for single input video
    """

    def __init__(self, path: str):
        self.video = os.path.join(path, "video_est.avi")

        # metric values will be calculated later
        self.metric_values = None

        # data structure
        json_dir = os.path.join(path, "json")
        self.data = jl.load_json(json_dir)

        # load images
        self.images = []
        image_dir = os.path.join(path, "images")
        image_list = os.listdir(image_dir)
        # temporary var
        first_frame = self.data[0]["ID"]
        # crop empty images
        cropped_image_list = image_list[first_frame:]
        last = first_frame
        iterator = 0
        for frame in self.data[1:]:
            frame_id = frame["ID"]
            offset = frame_id - last
            if offset > 1:
                iterator += offset - 1
            last = frame_id
            self.images.append(os.path.join(
                image_dir, cropped_image_list[iterator]))
            iterator += 1
        self.images.sort()

        # plot trajectories if they don't exist
        trajectory_dir = os.path.join(path, "trajectories")
        if not os.path.exists(trajectory_dir):
            os.mkdir(trajectory_dir)
            for keypoint in keypoints:
                plot_keypoint_trajectory(
                    self.data, keypoint, self.images[0], trajectory_dir)
        trajectory_list = os.listdir(trajectory_dir)
        self.trajectories = {}
        for file in trajectory_list:
            for keypoint in keypoints:
                if file.find(keypoint) != -1:
                    self.trajectories[keypoint_map[keypoint]] = (
                        os.path.join(trajectory_dir, file))
                    break
