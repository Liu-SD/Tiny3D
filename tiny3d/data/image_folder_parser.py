import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os.path as osp

from tiny3d.core import Module, Database
from tiny3d.utils.registry import register


@register("ImageFolderParser")
class ImageFolderParser(Module):
    """
    Load images and camera intrinsic from given `path`.
    Inputs:
        path: string. The path of image folder and intrinsics, in the format like NeRF dataset.
    """
    def __init__(self, database: Database, path: str):
        super().__init__(database)
        self.path = path

    def execute(self):
        print("ImageFolderParser skipped" )
        # image_name_list = glob(osp.join(self.path, 'rgb', '*.png'))
        # image_list = np.stack([plt.imread(image) for image in image_name_list])
        # intrinsic = self.read_intrinsics()
        # self.database.update_data({"image": image_list})
        # self.database.update_data({"image_name": image_name_list})
        # self.database.set_work_dir(self.path)
        # self.database.update_global_data({"intrinsic": intrinsic})

    def read_intrinsics(self):
        with open(osp.join(self.path, 'intrinsics.txt')) as f:
            fx = fy = float(f.readline().split()[0])
        w = h = int(800)

        K = np.float32([[fx, 0, w/2],
                        [0, fy, h/2],
                        [0,  0,   1]])
        return K


