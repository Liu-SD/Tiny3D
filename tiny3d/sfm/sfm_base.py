import numpy as np

from tiny3d.core import Module, Database
from tiny3d.utils.registry import register

@register("SfMBase")
class SfMBase(Module):
    """
    Base Structure from Motion implementation.
    """
    def __init__(self, database: Database):
        super().__init__(database)

    def execute(self):
        ### fake implementation
        poses = []
        for fname in self.database.get('image_name'):
            fname = fname.replace('rgb', 'pose').replace('png', 'txt')
            pose = np.loadtxt(fname)
            poses.append(pose)
        self.database.update_data({'pose': np.stack(poses)})
