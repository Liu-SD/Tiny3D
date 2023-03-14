import numpy as np

from tiny3d.core import Module, Database
from tiny3d.utils.registry import register

@register("PoseAdaptor")
class PoseAdaptor(Module):
    def __init__(self, database: Database):
        super().__init__(database)

    def vec2mat(self, ray_vec):
        ray_mat = np.zeros((3, 3))
        ray_mat[1,0] = ray_vec[2]; ray_mat[0,1] = -ray_vec[2]
        ray_mat[2,0] = -ray_vec[1]; ray_mat[0,2] = ray_vec[1]
        ray_mat[2,1] = ray_vec[0]; ray_mat[1,2] = -ray_vec[0]
        return ray_mat


    def execute(self):
        poses = self.database.get('pose')
        direction = np.array([0,0,1])
        rays_o = poses[:, :, 3]
        rays_d = direction[None, None, :] @ poses[:, :, :3].transpose((0,2,1))
        rays_d = rays_d.squeeze(1)
        A = []
        b = []
        for ray_o, ray_d in zip(rays_o, rays_d):
            a = self.vec2mat(ray_d)
            A.append(a)
            b.append((a @ ray_o[:, None]).squeeze(-1))
        A = np.concatenate(A, axis=0) # (3N,3)
        b = np.concatenate(b, axis=0) # (3N)
        p = np.linalg.lstsq(A, b, rcond=None)[0]
        assert np.all(np.sum((p - rays_o) * rays_d, axis=-1) > 0)
        poses[:, :, 3] -= p
        pose_radius = np.max(np.linalg.norm(poses[:, :, 3], axis=-1, ord=2))
        poses[:, :, 3] /= pose_radius

        # import matplotlib.pyplot as plt
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        # ax.quiver(rays_o[:, 0], rays_o[:, 1], rays_o[:, 2], rays_d[:, 0], rays_d[:, 1], rays_d[:, 2], length=0.1, color='green')
        # ax.scatter(0, 0, 0)
        # plt.show()

        self.database.update_data({"pose": poses})
