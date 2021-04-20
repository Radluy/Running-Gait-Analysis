import os
import json_load as jl
from trajectory import plot_keypoint_trajectory


keypoints = ["RKnee", "LKnee", "LAnkle", "RAnkle", "Neck", "MidHip"]
keypoint_map = {
    "RKnee": "Right Knee",
    "LKnee": "Left Knee",
    "Neck": "Neck",
    "MidHip": "Middle of hips",
    "RAnkle": "Right Ankle",
    "LAnkle": "Left Ankle",
}

class folderStruct():

    def __init__(self, path: str):
        self.video = os.path.join(path, "video_est.avi")
        self.metric_values = None

        json_dir = os.path.join(path, "json")
        self.data = jl.load_json(json_dir)

        #temporary var
        first_frame = self.data[0]["ID"]

        self.images = []
        image_dir = os.path.join(path, "images")
        image_list = os.listdir(image_dir)
        # crop empty images
        cropped_image_list = image_list[first_frame:len(self.data)+first_frame]
        for file in cropped_image_list:
            self.images.append(os.path.join(image_dir,file))
        self.images.sort()

        trajectory_dir = os.path.join(path, "trajectories")
        if not os.path.exists(trajectory_dir):
             os.mkdir(trajectory_dir)
             for keypoint in keypoints:
                plot_keypoint_trajectory(self.data, keypoint, self.images[0], trajectory_dir)
        trajectory_list = os.listdir(trajectory_dir)
        self.trajectories = {}
        for file in trajectory_list:
            for keypoint in keypoints:
                if file.find(keypoint) != -1:
                    self.trajectories[keypoint_map[keypoint]] = (os.path.join(trajectory_dir, file))
                    break
        
        
