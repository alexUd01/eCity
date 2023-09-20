#!/usr/bin/python3
"""A module containing User class"""
from .storage_engine.dbstorage import db
from datetime import datetime
from ecity.models.base_model import BaseModel
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
    logged_in = db.Column(db.Enum('T', 'F'), nullable=False)
    teacher_id = db.Column(db.Integer, nullable=True)
    dp = db.Column(db.String(256), nullable=True,
                   server_default="profile-icon.png")

    def get_students(self):
        """ Returns a list of students linked to this user """
        students = User.query.filter(
            User.teacher_id == self.user_id).all()
        return students
