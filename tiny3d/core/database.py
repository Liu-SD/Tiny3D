from collections import OrderedDict

from tiny3d.utils.logger import get_logger

class Database(object):
    def __init__(self) -> None:
        self._data_dict = OrderedDict()
        self._global_data_dict = OrderedDict()
        self._data_length = None
        self.logger = get_logger()

    def update_data(self, update_dict: dict):
        self._data_dict.update(update_dict)
        for k, v in update_dict.items():
            if self._data_length is None:
                self._data_length = len(v)
            elif self._data_length != len(v):
                self.logger.warn(f"Data length no equal! Length of key {k} is {len(v)}, but database length is {self._data_length}.")


    def update_global_data(self, update_dict: dict):
        self._global_data_dict.update(update_dict)

    def get(self, key):
        if isinstance(key, str):
            key = [key]
        v = []
        for k in key:
            if k in self._global_data_dict:
                v.append(self._global_data_dict[k])
            elif k in self._data_dict:
                v.append(self._data_dict[k])
            else:
                self.logger.warn(f"Key {k} not exist!")
        if len(v) == 1:
            return v[0]
        return v
