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

    @classmethod
    def remove(cls):
        """
        A class method that removes instances of its class identified by 'id'
        """
        from .user import User
        from .exam import Exam
        from .question import Question
        from .answer import Answer
        from .answer_sheet import AnswerSheet
        from .score import Score

        mapper = {
            'User': User,
            'Exam': Exam,
            'Question': Question,
            'Answer': Answer,
            'AnswerSheet': AnswerSheet,
            'Score': Score
        }
        cls_name = cls.__class__.__name__
        pass  # TODO: Same concept different function
