import importlib
import os

subfolders = ['data', 'sfm', 'nerf']
for subfolder in subfolders:
    arch_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), subfolder)
    arch_filenames = [os.path.splitext(v)[0] for v in os.listdir(arch_folder) if v.endswith('.py')]
    # import all the arch modules
    [importlib.import_module(f'tiny3d.{subfolder}.{file_name}') for file_name in arch_filenames]
__all__ = []
