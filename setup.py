from distutils.core import setup
from setuptools import find_packages

setup(name='tiny3d',
      version='0.1',
      description='Tiny 3D reconstruction library.',
      author='Sidun Liu',
      packages=find_packages(exclude='script'),
    )

