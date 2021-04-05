import os


class folderStruct():

    def __init__(self, path: str):
        self.images = []
        image_dir = os.path.join(path, "images")
        image_list = os.listdir(image_dir)
        for file in image_list:
            self.images.append(os.path.join(image_dir,file))
