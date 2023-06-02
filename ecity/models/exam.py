#!/usr/bin/python3
"""A module containing Exam class"""
from ecity.app.ecity_app import db
from datetime import datetime
from ecity.models.base_model import BaseModel
from ecity.models.question import Question


class Exam(BaseModel, db.Model):
    """ Exam Table """
    exam_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(128), nullable=False)
    time_allowed = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow())
    date_taken = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)
    examiner = db.relationship('User', backref='exams')

    def count(self):
        """ Returns the number of questions in a database for an exam """
        count_questions = Question.query.filter(
            Question.exam_id==self.exam_id).count()
        return count_questions

    def all_questions(self):
        """ Returns all question objects with question.exam_id==self.exam_id
        """
        questions = Question.query.filter(
            Question.exam_id==self.exam_id).all()

        all_q_as_list_of_dict = []
        for obj in questions:
            enhanced_obj = obj.to_dict()
            enhanced_obj['options'] = obj.available_options()
            all_q_as_list_of_dict.append(enhanced_obj)
        print(all_q_as_list_of_dict[5])
        return all_q_as_list_of_dict
