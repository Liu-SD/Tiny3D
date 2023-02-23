from typing import Callable

from tiny3d.core import Module
from tiny3d.utils.logger import get_logger


class ModuleFactory(object):
    registry = dict()

    @classmethod
    def register_module(cls, name: str) -> Callable:
        def inner_wrapper(wrapped_class: Module) -> Callable:
            if not issubclass(wrapped_class, Module):
                get_logger().warn(f'Expect module {name} to be type Module, but got {wrapped_class}.')
            if name in cls.registry:
                get_logger().warn(f'Module {name} already exists. Will replace it.')
            cls.registry[name] = wrapped_class
            return wrapped_class
        return inner_wrapper

    @classmethod
    def create_module(cls, name: str, **kwargs) -> Module:
        if name not in cls.registry:
            get_logger().warn(f'Module {name} does not eist in the registry.')
            return None
        return cls.registry[name](**kwargs)

def register(module):
    return ModuleFactory.register_module(module)
