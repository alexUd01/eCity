#!/usr/bin/python3
"""A module containing Question class"""
from .storage_engine.dbstorage import db
from datetime import datetime
from ecity.models.base_model import BaseModel


class Question(BaseModel, db.Model):
    """Question Table"""
    question_id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.Text, nullable=False)

    A = db.Column(db.Text, nullable=True)
    B = db.Column(db.Text, nullable=True)
    C = db.Column(db.Text, nullable=True)
    D = db.Column(db.Text, nullable=True)
    E = db.Column(db.Text, nullable=True)
    F = db.Column(db.Text, nullable=True)
    G = db.Column(db.Text, nullable=True)
    H = db.Column(db.Text, nullable=True)

    exam_id = db.Column(db.Integer, db.ForeignKey('exam.exam_id'),
                          nullable=False)
    exam = db.relationship('Exam', backref='questions')

    def available_options(self, permutate=True):
        opt_avail = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
        """ Returns all available options """
        if permutate is False:
            print("Not Implemented yet!")
            pass # Implement later
        else:
            options = {}
            for k, v in self.__dict__.copy().items():
                if k in opt_avail and v is not None:
                    options[k] = v
            return options
