import os
import json_load as jl

class folderStruct():

    def __init__(self, path: str):
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

        
        
