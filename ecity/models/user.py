#!/usr/bin/python3
"""A module containing User class"""
from .storage_engine.dbstorage import db
from datetime import datetime
from ecity.models.base_model import BaseModel
from ecity.models.answer_sheet import AnswerSheet
from flask_login import UserMixin


class User(UserMixin, BaseModel, db.Model):
    """User table"""
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    firstname = db.Column(db.String(128), nullable=False,
                          server_default='guest')
    lastname = db.Column(db.String(128), nullable=False,
                         server_default='guest')
    middlename = db.Column(db.String(128), nullable=False,
                           server_default='guest')
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), nullable=False,
                      server_default='guest@ecity.com',
                      unique=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    is_student = db.Column(db.Enum('T', 'F'), nullable=True)
    is_examiner = db.Column(db.Enum('T', 'F'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    last_login = db.Column(db.DateTime, nullable=True)
    last_logout = db.Column(db.DateTime, nullable=True)
    logged_in = db.Column(db.Enum('T', 'F'), nullable=False)
    teachers = db.Column(db.Text, nullable=True)
    students = db.Column(db.Text, nullable=True)
    dp = db.Column(db.String(256), nullable=True,
                   server_default="profile-icon.png")

    def completed_exams(self):
        """ Returns a list exam_id's of user completed exams """
        answer_sheets = AnswerSheet.query.filter(
            AnswerSheet.user_id == self.user_id).all()
        exam_ids = []
        for answer_sheet in answer_sheets:
            if answer_sheet.exam_id not in exam_ids:
                exam_ids.append(answer_sheet.exam_id)
        return exam_ids

    def get_students(self):
        """ Returns a list of students linked to this user """
        students = []
        if self.is_examiner == 'T':
            try:
                students_ids = eval(self.students)
            except SyntaxError:
                students_ids = ()
            for _id in students_ids:
                student = User.query.filter(User.user_id == _id).one()
                students.append(student)
        return students

    def add_student(self, student_id):
        """ adds a student's user_id to 'user.students' """
        if self.is_examiner == 'T':
            self.students = f"{self.students}, {student_id},"
            return True
        return False

    def get_teachers(self):
        """
        Returns a list of teachers linked to `user` if `user` is a student
        """
        teachers = []
        if self.is_student == 'T':
            try:
                teachers_ids = eval(self.teachers)
            except SyntaxError:
                teachers_ids = ()
            for _id in teachers_ids:
                teacher = User.query.filter(User.user_id == _id).one()
                teachers.append(teacher)
        return teachers

    def add_teacher(self, teacher_id):
        """ adds a student's user_id to 'user.students' """
        if self.is_student == 'T':
            self.teacher = f"{self.teacher}, {teacher_id},"
            return True
        return False
