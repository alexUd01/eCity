#!/usr/bin/python3
"""A module containing Answer class"""
from ecity.app.ecity_app import db
from datetime import datetime
from ecity.models.base_model import BaseModel

class Answer(BaseModel, db.Model):
    """Answer Table"""
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'),
                            nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.exam_id'),
                          nullable=False)
    correct_option = db.Column(db.String(1), nullable=True)
    correct_notes = db.Column(db.Text, nullable=True)

    question = db.relationship('Question', backref='answer')
