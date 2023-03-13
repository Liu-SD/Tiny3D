from pathlib import *

import numpy as np
import matplotlib.pyplot as plt
import pycolmap
import transformations

from tiny3d.core import Module, Database
from tiny3d.utils.registry import register

import sys


@register("SfMBase")
class SfMBase(Module):
    """
    Base Structure from Motion implementation.
    """
    def __init__(self, database: Database,path: str):
        super().__init__(database)
        self.path = path
        self.image_name_list = []
        self.poses = []
        self.intrinsics = []        ## More than one intrinsic may exist

    def read_poses(self, path) :
        image_txt_path = path + "/sparse/colmap/images.txt"
        output_poses_dir = path + "/pose"
        if not Path(output_poses_dir).exists():
            Path(output_poses_dir).mkdir()
        with open(image_txt_path) as f:
            idx = 0
            for line in f:
                if line.startswith("#"):
                    continue
                idx += 1
                if idx % 2 == 0:
                    continue
                line = line.split()
                quat = np.array([float(i) for i in line[1:5]])
                t = np.array([float(i) for i in line[5:8]])
                name = line[-1]             #100_7104.JPG
                self.image_name_list.append(path + "/images/" +name)
                name = name.split('.')[0] + '.txt'
                r = transformations.quaternion_matrix(quat)
                t_mat = np.eye(4)
                t_mat[:3, 3] = -t
                pose = r.T @ t_mat
                output_poses_path = output_poses_dir + f"/{name}"
                np.savetxt(output_poses_path, pose)
                self.poses.append(pose)

    def read_intrinsics(self, path) :
        cameras_txt_path = path + "/sparse/colmap/cameras.txt"
        output_poses_dir = path + "/intrinsic"
        if not Path(output_poses_dir).exists():
            Path(output_poses_dir).mkdir()
        with open(cameras_txt_path) as f:
            cameras_id = 1
            idx = 0
            for line in f:
                if line.startswith("#"):
                    continue
                idx += 1
                if idx % 2 == 0:
                    continue
                line = line.split()
                intrinsic = np.array([float(i) for i in line[2:8]])
                K = np.float32( [[intrinsic[2],               0,   intrinsic[3]],
                                [           0,    intrinsic[4],   intrinsic[5]],
                                [           0,               0,              1]])
                output_poses_path = output_poses_dir + f"/intrinsic_{cameras_id}.txt"
                np.savetxt(output_poses_path, K)
                self.intrinsics.append(K)

    def execute(self):
        ### colmap for sfm
        self.database.set_work_dir(self.path)

        work_dir  = self.path
        image_dir = Path(work_dir) / "images"
        output_path = Path(work_dir) / "sparse"

        if not output_path.exists():
            output_path.mkdir()

        database_path = output_path / "database.db"

        if not database_path.exists():
            pycolmap.extract_features(database_path, image_dir)
            pycolmap.match_exhaustive(database_path)
            maps = pycolmap.incremental_mapping(database_path, image_dir, output_path)
            if not (output_path/ "colmap").exists():
                (output_path/ "colmap").mkdir()
            maps[0].write_text((output_path/ "colmap").__str__())

        self.read_poses(work_dir)
        self.read_intrinsics(work_dir)

        image_list = np.stack([plt.imread(image) for image in self.image_name_list])
        self.database.update_data({"image": image_list})
        self.database.update_data({"image_name": self.image_name_list})

        ### updata poses
        self.database.update_data({"pose": np.stack(self.poses)})
        self.database.update_global_data({"intrinsic": self.intrinsics})    #








