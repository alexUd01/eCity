#!/usr/bin/python3
"""A module containing User class"""
from ecity.app.ecity_app import db
from datetime import datetime
from ecity.models.base_model import BaseModel


class User(BaseModel, db.Model):
    """User table"""
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    firstname = db.Column(db.String(128), nullable=False, default='guest')
    lastname = db.Column(db.String(128), nullable=False, default='guest')
    middlename = db.Column(db.String(128), nullable=False, default='guest')
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), nullable=False, default='guest',
                      unique=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    is_student = db.Column(db.Enum('T', 'F'), nullable=True)
    is_examiner = db.Column(db.Enum('T', 'F'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
