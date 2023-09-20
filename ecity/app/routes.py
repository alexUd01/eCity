#!/usr/bin/python3
"""eCity Routes"""
from datetime import datetime, timedelta, date, time
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

db_url = 'mysql+mysqldb://alex:kalixan01@localhost/ecity'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex().encode()

lm.init_app(app)  # Initialize login manager for `app`
db.init_app(app)  # Initialize database handle for `app`
flask.globals.CURR_USER = None

available_options = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

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
    student_login = request.args.get('student_login')
    if student_login == 'True':
        return render_template('login.html', student_login=True)
    else:
        return render_template('login.html')


@app.route('/sign-in', strict_slashes=False, methods=['POST'])
def sign_in():
    """ Landing Page """
    student_login = request.form.get('student_login')
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
                db.object_session(user).commit()
                login_user(user, duration=timedelta(seconds=30))
                flask.globals.CURR_USER = user
                flash('Successfully signed-in. Welcome back 🙂', 'success')
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
    exams = Exam.query.filter(Exam.user_id == user_id).all()
    uniq_exams = []
    for exam in exams:
        timestamp = "{}T{}.000000".format(exam.exam_date, exam.end_time)
        exam_end_datetime = datetime.fromisoformat(timestamp)
        if exam_end_datetime > datetime.now():
            exam.exam_end_datetime = exam_end_datetime
            uniq_exams.append(exam)
    uniq_exams.sort(key=lambda exam: exam.exam_end_datetime)
    return render_template('dashboard.html', user=user,
                           exams=uniq_exams, date=date)


@app.route('/users/<int:user_id>/past_exams', strict_slashes=False)
@login_required
def past_exams(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    exams = Exam.query.filter(Exam.user_id == user_id).all()
    uniq_exams = []
    for exam in exams:
        timestamp = "{}T{}.000000".format(exam.exam_date, exam.end_time)
        exam_end_datetime = datetime.fromisoformat(timestamp)
        if exam_end_datetime < datetime.now():
            exam.exam_end_datetime = exam_end_datetime
            uniq_exams.append(exam)
    uniq_exams.sort(key=lambda exam: exam.exam_end_datetime, reverse=True)
    return render_template('dashboard_past_exams.html', user=user,
                           exams=uniq_exams, date=date)


@app.route('/users/<int:user_id>/my_students', strict_slashes=False)
@login_required
def my_students(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_my_students.html', user=user,
                           len=len)


@app.route('/users/<int:user_id>/manage_exams', strict_slashes=False)
@login_required
def manage_exams(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    exams = Exam.query.filter(Exam.user_id == user_id).all()
    return render_template('dashboard_manage_exams.html', user=user,
                           date=date, time=time, datetime=datetime,
                           exams=exams)


@app.route('/users/<int:user_id>/manage_exams/create_exam_template',
           methods=['POST'], strict_slashes=False)
@login_required
def create_exam_template(user_id):
    """ Creates an examination """
    course_name = str(request.form.get('course_name'))
    no_of_questions = int(request.form.get('no_of_questions'))
    time_allowed = int(request.form.get('time_allowed'))
    exam_date = date.fromisoformat(request.form.get('exam_date'))
    start_time = time.fromisoformat(request.form.get('start_time'))
    end_time = time.fromisoformat(request.form.get('end_time'))
    examiner_name = str(request.form.get('examiner_name'))
    date_created = datetime.utcnow()
    user = User.query.filter(User.user_id == user_id).one()
    return render_template(
        'manage_exams/create_exam_template.html', user=user,
        course_name=course_name, no_of_questions=no_of_questions,
        time_allowed=time_allowed, exam_date=exam_date, start_time=start_time,
        end_time=end_time, date_created=date_created, date=date,
        datetime=datetime
    )


@app.route('/users/<int:user_id>/manage_exams/edit_exam_template',
           methods=['GET', 'POST'], strict_slashes=False)
#@login_required
def edit_exam_template(user_id):
    """ Creates a template for setting an examination """
    exam_id = request.args.get('exam_id')
    if not exam_id:
        flash('Exam id not provided.', 'error')
        return redirect(url_for('manage_exams', user_id=user_id))

    user = User.query.filter(User.user_id == user_id).one()
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    questions = Question.query.filter(Question.exam_id == exam_id).all()
    for question in questions:
        answer = Answer.query.filter(
            Answer.question_id == question.question_id).one()
        setattr(question, 'answer', [answer])

    if request.method == 'POST':
        try:
            exam.no_of_questions = int(request.form.get('no_of_questions'))
        except Exception:
            raise
        else:
            db.commit()
    return render_template(
        'manage_exams/edit_exam_template.html', user=user, exam=exam,
        questions=questions, date=date, datetime=datetime, len=len
    )


@app.route('/users/<int:user_id>/manage_exams/<string:instruction>',
           methods=['POST'], strict_slashes=False)
@login_required
def create_or_edit_exam(user_id, instruction):
    """ Creates or edits an examination """
    successful = False
    if instruction == 'create_exam':
        course_name = str(request.form.get('course_name'))
        no_of_questions = int(request.form.get('no_of_questions'))
        time_allowed = int(request.form.get('time_allowed'))
        exam_date = date.fromisoformat(request.form.get('exam_date'))
        start_time = time.fromisoformat(request.form.get('start_time'))
        end_time = time.fromisoformat(request.form.get('end_time'))
        examiner_name = str(request.form.get('examiner_name'))
        date_created = datetime.utcnow()
        exam = Exam(
            course_name=course_name, no_of_questions=no_of_questions,
            time_allowed=time_allowed, exam_date=exam_date,
            start_time=start_time, date_created=date_created,
            end_time=end_time, user_id=user_id
        )
        try:  # Prepare Exam
            db.add(exam)
            db.object_session(exam).commit()
        except Exception:
            db.rollback()
            raise
        else:
            print(f"Created a new exam with id: {exam.exam_id}")
            for i in range(1, no_of_questions + 1):
                data = request.form.get(f'Q{i}')
                _dict = {'data': data, 'exam_id': exam.exam_id}
                for opt in available_options:
                    _dict[opt] = request.form.get(f'Q{i}-option-{opt}')
                    if _dict[opt] in ['', 'None']:
                        _dict[opt] = None
                question = Question(**_dict)
                try:
                    db.add(question)
                    db.object_session(question).commit()
                except Exception:
                    db.rollback()
                    raise
                else:
                    print("Created a new question with id: {}".format(
                        question.question_id
                    ))
                    correct_option = str(request.form.get(
                        f'Q{i}-correct_option')).upper()
                    correct_notes = str(request.form.get(
                        f'Q{i}-correct_notes'
                    ))
                    _ans_dict = {
                        'correct_option': correct_option,
                        'correct_notes': correct_notes,
                        'question_id': question.question_id,
                        'exam_id': question.exam_id
                    }
                    answer = Answer(**_ans_dict)
                    db.add(answer)
                    db.object_session(answer).commit()
                    successful = True
            if successful:
                flash(
                    f"""Examination successfully scheduled for {exam_date}
                    by {start_time}.""", 'success'
                )
            else:
                flash("Couldnt create exam something went wrong", 'error')
        return redirect(url_for('manage_exams', user_id=user_id))
    elif instruction == 'edit_exam':
        exam_id = int(request.form.get('exam_id'))
        if not exam_id:
            flash("ERROR: FOR ADIM PURPOSE ONLY: Invalid exam id sent", 'error')
            return redirect(url_for('manage_exams', user_id=user_id))
        exam = Exam.query.filter(Exam.exam_id == exam_id).one()
        try:  # Collect Exam details
            exam.course_name = str(request.form.get('course_name'))
            exam.no_of_questions = int(request.form.get('no_of_questions'))
            exam.time_allowed = int(request.form.get('time_allowed'))
            exam.exam_date = date.fromisoformat(request.form.get('exam_date'))
            exam.start_time = time.fromisoformat(request.form.get('start_time'))
            exam.end_time = time.fromisoformat(request.form.get('end_time'))
            exam.examiner_name = str(request.form.get('examiner_name'))
            exam.date_updated = datetime.utcnow()
            db.object_session(exam).commit()
        except Exception:
            db.rollback()
            raise
        else:
            print(f"Edited a new exam with id: {exam.exam_id}")
            old_questions = Question.query.filter(
                Question.exam_id == exam_id).all()
            for i in range(exam.no_of_questions):
                question_id = request.form.get(f'Q{i}-id')
                if question_id in ["", 'None', None]:
                    # User wants to add new questions to exam
                    data = str(request.form.get(f'Q{i}'))
                    _dict = {'data': data, 'exam_id': exam_id}
                    for opt in available_options:
                        val = request.form.get(f'Q{i}-option-{opt}')
                        if val in ["", 'None']:
                            val = None
                        _dict[opt] = val
                    question = Question(**_dict)
                    db.add(question)
                    db.object_session(question).commit()
                    # Collect correct option
                    correct_option = str(request.form.get(
                        f'Q{i}-correct_option')).upper()
                    correct_notes = str(request.form.get(
                        f'Q{i}-correct_notes'))
                    _ans_dict = {
                        'correct_option': correct_option,
                        'correct_notes': correct_notes,
                        'question_id': question.question_id,
                        'exam_id': exam_id
                    }
                    answer = Answer(**_ans_dict)
                    db.add(answer)
                    db.object_session(answer).commit()
                    successful = True
                    pass
                else:  # User edited a pre-existing question
                    question_id = int(question_id)
                    question = list(
                        filter(lambda obj: int(obj.question_id) == question_id,
                               old_questions)
                    )[0]
                    question.data = request.form.get(f'Q{i}')
                    for opt in available_options:
                        val = request.form.get(f'Q{i}-option-{opt}')
                        if val in ["", 'None']:
                            val = None
                        setattr(question, opt, val)
                    db.object_session(question).commit()
                    answer_id = int(request.form.get(f'Q{i}-correct-option-id'))
                    answer = Answer.query.filter(
                        Answer.answer_id == answer_id).one()
                    answer.correct_option = request.form.get(
                        f'Q{i}-correct_option').upper()
                    answer.correct_notes = request.form.get(
                        f'Q{i}-correct_notes')
                    db.object_session(answer).commit()
                    successful = True
                    pass
            # Finished updating exam's, questions' and answer's tables rspctvly
            for question in old_questions:
                print("Updated a question with id: {}\n{}".format(
                    question.question_id, question
                ))
        if successful:
            flash("Examination successfully updated.", 'success')
        else:
            flash("Could not update exam something went wrong", "error")
        # print(dir(db))
        return redirect(url_for('manage_exams', user_id=user_id))
    else:
        abort(404)


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
        db.object_session(user).commit()
        flask.globals.CURR_USER = None
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))
