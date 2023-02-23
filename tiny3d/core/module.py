from tiny3d.core import Database
from tiny3d.utils.logger import get_logger

class Module(object):
    """
    Please make a description on current module and arguments.
    """
    def __init__(self, database: Database):
        self.database = database
        self.logger = get_logger()

    def execute(self):
        raise NotImplementedError
