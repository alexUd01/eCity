#!/usr/bin/python3
"""eCity Routes"""
from flask import Flask, redirect, url_for, render_template, request, abort
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_url = 'mysql+mysqldb://User3:password@localhost/ecity'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from ecity.models.user import User
from ecity.models.exam import Exam
from ecity.models.question import Question
from ecity.models.answer import Answer


@app.errorhandler(404)
def err_404(err_no):
    return jsonify({"error":"Not found"})

@app.route('/', strict_slashes=False)
def index():
    """ Landing Page """
    # If user is new_user display new_user page
    # else if redirected from login, take old_user to his account
    return "Welcome\n"

@app.route('/login', strict_slashes=False)
def login():
    """ Landing Page """
    # if request.form['user'] exists and request.form['password'] == user_pass
    # log user into his account
    return redirect(url_for('index'))

@app.route('/test_exam', strict_slashes=False)
def test_exam_page():
    """Delete this route after test"""
    user1 = User.query.filter(User.username=='Raymonis').first()
    exam1 = Exam.query.filter(Exam.exam_id=='1').first()
    return render_template('exam_base.html', user=user1, exam=exam1)

@app.route('/test_exam/<int:exam_id>/', strict_slashes=False)
def exam(exam_id=None):
    """Returns an exam object"""
    if exam_id is None:
        abort(404)
    try:
        exam = Exam.query.filter(Exam.exam_id==exam_id).one()
    except Exception:
        return "No question found!", 404
    return exam.all_questions()
