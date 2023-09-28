#!/usr/bin/python3
"""A module containing AnswerSheet class"""
from .storage_engine.dbstorage import db
from datetime import datetime
from ecity.models.base_model import BaseModel


class AnswerSheet(BaseModel, db.Model):
    """AnswerSheet table"""
    answer_sheet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.exam_id'),
                        nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'),
                            nullable=False)
    student_choice = db.Column(db.String(1), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())

    user = db.relationship('User', backref="answer_sheets")
    exam = db.relationship('Exam', backref="answer_sheets")
    question = db.relationship('Question', backref="answer_sheets")
