# import pytorch_lightning as pl
import sys

from tqdm import tqdm
import time

from tiny3d.core import Module, Database
from tiny3d.utils.registry import register
from tiny3d.nerf.utils import torch_dataset_from_database

# class NeRF(pl.LightningModule):
#     pass

@register("NeRFBase")
class NeRFBase(Module):
    def __init__(self, database: Database, **kwargs):
        super().__init__(database)
        dataset = torch_dataset_from_database(database, keys=['image', 'pose'])
        dataset.intrinsic = database.get('intrinsic')
        # self.pl_model = NeRF()

    def execute(self):
        self.logger.info("Start NeRF training!")
        # fake implementation
        for _ in tqdm(range(100)):
            time.sleep(0.1)
        self.logger.info("Training Finished.")
