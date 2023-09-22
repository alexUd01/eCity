#!/usr/bin/python3
"""A module containing scores class"""
from .storage_engine.dbstorage import db
from datetime import datetime
from ecity.models.base_model import BaseModel


class Score(BaseModel, db.Model):
    """Score table"""
    score_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.exam_id'),
                        nullable=False)
    score = db.Column(db.Integer, nullable=False)
    score_attainable = db.Column(db.Integer, nullable=False)
