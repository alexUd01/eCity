#!/usr/bin/python3
"""A module containing BaseModel class"""


class BaseModel:
    """Definition for repr"""
    def __repr__(self):
        """Pretty print"""
        return "<{}: {}>".format(type(self).__name__, self.__dict__)

    def to_dict(self):
        """Convert instances on various objects to dict"""
        avail_opts = ('A', 'B', 'C', 'D', 'D', 'E', 'F', 'G', 'H')
        new_dict = {}
        options = []
        for key, val in self.__dict__.items():
            if key == "_sa_instance_state" or key in avail_opts:
                continue
            new_dict[key] = val
        return new_dict
