#!/usr/bin/python3
"""eCity Routes"""
from datetime import datetime, timedelta
from uuid import uuid4
import secrets
from ecity.models.user import User
from ecity.models.exam import Exam
from ecity.models.question import Question
from ecity.models.answer import Answer
from ecity.models.answer_sheet import AnswerSheet
from ecity.models.score import Score
import flask
from flask import Flask, redirect, url_for, g, render_template, request, abort
from flask import jsonify, make_response, flash, get_flashed_messages
from ..models.storage_engine.dbstorage import db
from .login_manager import *
from sqlalchemy.exc import IntegrityError, NoResultFound

app = Flask(__name__)

db_url = 'mysql+mysqldb://User3:password@localhost/ecity'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex().encode()

lm.init_app(app)  # Initialize login manager for `app`
db.init_app(app)  # Initialize database handle for `app`
flask.globals.CURR_USER = None

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(e._message())
        quit()
    else:
        db = db.session()
        # db.add_all([person1, person2])


@app.teardown_appcontext
def close_db(var):
    """ Close connection to database """
    db.commit()
    db.close()


@app.errorhandler(404)
def err_404(err_no):
    return jsonify({"error": "Not found"})


@app.before_request
def before_request():
    """ Executed before each request """
    g.uuid4 = uuid4


@lm.user_loader
def load_user(user_id):
    """ Loads user """
    try:
        user = User.query.filter(User.user_id == user_id).one()
    except NoResultFound:
        return None
    else:
        user.id = user.user_id
        flask.globals.CURR_USER = user
        return user


@lm.unauthorized_handler
def unauthorized_err_401():
    """ Handles unauthorized error """
    logout_user()
    flash('You must be logged in to access the requested resource.', 'error')
    return redirect(url_for('login'))


@app.route('/', strict_slashes=False)
@app.route('/index/', strict_slashes=False)
def index():
    """ Landing Page """
    # If user is new_user display new_user page
    # else if redirected from login, take old_user to his account
    return render_template('index.html')


@app.route('/sign-up', strict_slashes=False)
def sign_up():
    """ Sign-up Page """
    return render_template('sign_up.html')


@app.route('/create-account', strict_slashes=False, methods=['POST'])
def create_user():
    """ Creates a user account """
    u_name = request.form['username']
    f_name = request.form['firstname']
    l_name = request.form['lastname']
    m_name = request.form['middlename']
    email = request.form['email']
    psword = request.form['password']

    user = User(username=u_name, firstname=f_name, lastname=l_name,
                middlename=m_name, email=email, password=psword,
                last_login=datetime.utcnow(), logged_in='T')
    user.id = user.user_id
    try:
        db.add(user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if 'email' in e._message():
            flash(
                f"""User account with email <i>"{email}</i>" already
                exists.<br>
                If you\'re the owner of the account please login instead.
                """,
                'error'
            )
        elif 'username' in e._message():
            flash(
                f"""User account with username <i>"{u_name}</i>" already
                exists.<br>If you\'re the owner of the account please login
                instead.""",
                'error'
            )
        return redirect(url_for('sign_up'))
    except Exception:
        db.rollback()
        flash(
            """A server side error just occured. Please notify the
            system administrator at "<i>alexanderikpeama@gmail.com</i>".
            """,
            'error')
    else:
        user = User.query.filter(User.user_id == user.user_id).one()
        user.id = user.user_id
        login_user(user, duration=timedelta(days=30))
        flash(
            f"""Welcome to eCity {user.firstname} {user.lastname}.
            If you need help in setting-up your workspace, don't hesitate
            to contact our support centre at alexanderikpeama@gmail.com
            """, 'success')
        return redirect(url_for('dashboard', user_id=user.user_id))


@app.route('/login', strict_slashes=False)
def login():
    """ Login Page """
    return render_template('login.html')


@app.route('/sign-in', strict_slashes=False, methods=['GET', 'POST'])
def sign_in():
    """ Landing Page """
    if request.method == 'GET':
        guest = User.query.filter(User.username == 'guest').one()
        return redirect(url_for('dashboard', user_id=guest.user_id))

    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return redirect(url_for('login'))

    try:
        user = User.query.filter(User.username == username).one()
    except Exception as e:
        flash('There is no account associated with the username you provided.',
              'warning')
        return redirect(url_for('login'))
    else:
        if password == user.password:
            user.id = user.user_id
            if flask.globals.CURR_USER and user == flask.globals.CURR_USER:
                flash('You are already signed-in.', 'success')
                login_user(user, duration=timedelta(seconds=30))
                return redirect(url_for('dashboard', user_id=user.user_id))
            else:
                user.last_login = datetime.utcnow()
                # TODO: fix failure to update last_login in db
                print(user.last_login)
                user.logged_in = 'T'
                db.commit()
                login_user(user, duration=timedelta(seconds=30))
                flask.globals.CURR_USER = user
                flash('Successfully signed-in.Welcome 🙂', 'success')
                return redirect(url_for('dashboard', user_id=user.user_id))
        else:
            flash('The password you entered is incorect. '
                  'Please enter the correct password.', 'warning')
            return redirect(url_for('login'))


@app.route('/users/<int:user_id>/dashboard', strict_slashes=False)
@app.route('/users/<int:user_id>/upcoming_exams', strict_slashes=False)
@login_required
def dashboard(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard.html', user=user)


@app.route('/users/<int:user_id>/past_exams', strict_slashes=False)
@login_required
def past_exams(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_past_exams.html', user=user)


@app.route('/users/<int:user_id>/my_students', strict_slashes=False)
@login_required
def my_students(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_my_students.html', user=user)


@app.route('/users/<int:user_id>/manage_exams', strict_slashes=False)
@login_required
def manage_exams(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_manage_exams.html', user=user)


@app.route('/test_exam', strict_slashes=False)
@login_required
def test_exam_page():
    """Delete this route after test"""
    user1 = User.query.filter(User.username == 'guest').first()
    exam1 = Exam.query.filter(Exam.exam_id == '1').first()
    return render_template('exam_base.html', user=user1, exam=exam1)


@app.route('/test_exam/<int:exam_id>/', strict_slashes=False)
@login_required
def exam(exam_id=None):
    """Returns an exam object"""
    if exam_id is None:
        abort(404)
    try:
        exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    except Exception:
        return "No question found!", 404
    return exam.all_questions()


@app.route('/users/<int:user_id>/exams/', methods=['POST'],
           strict_slashes=False)
@login_required
def user(user_id=None):
    """Does some stuff"""
    raw_ans_sheet = dict(request.form)
    user_id = request.form['user_id']
    exam_id = request.form['exam_id']
    question_id = None
    answers_list = []
    i = 0
    for k, v in raw_ans_sheet.items():
        try:
            question_id = k.strip(']').split('[')[1]
        except IndexError:
            pass
        else:
            answers_list.append(
                AnswerSheet(user_id=user_id, exam_id=exam_id,
                            question_id=question_id, student_choice=v)
            )
            i += 1

    db.add_all(answers_list)
    db.commit()
    exam_score, score_attainable = create_scores(answers_list, exam_id)
    score = Score(user_id=user_id, exam_id=exam_id, score=exam_score,
                  score_attainable=score_attainable)
    db.add(score)
    db.commit()
    return redirect(url_for('index'))  # I don't yet know what this does yet


def create_scores(answers_list, exam_id):
    """ A function that adds scores to the score table """
    exam_score = 0
    correct_answers = Answer.query.filter(Answer.exam_id == exam_id).all()
    for ans_sheet in answers_list:
        for item in correct_answers:
            if ans_sheet.question_id == item.question_id:
                # print(item.question_id, item.correct_option,
                # ans_sheet.student_choice)
                if ans_sheet.student_choice == item.correct_option:
                    exam_score += 1
                    break
    return exam_score, len(correct_answers)

@app.route('/logout', strict_slashes=False)
def logout():
    """
    Please not that this logout feature does not yet include support for total
    logout from all browsing sessions across different web clients.
    It's still a work in progress
    """
    logout_user()
    user = flask.globals.CURR_USER
    if user:
        user.logged_in = 'F'
        db.commit()
        flask.globals.CURR_USER = None
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))
