#!/usr/bin/python3
"""eCity Routes"""
import time as t
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
from sqlalchemy.exc import IntegrityError, NoResultFound, InvalidRequestError
from os import getcwd, system
import os
from bcrypt import hashpw, checkpw, gensalt
import json
from json.decoder import JSONDecodeError

app = Flask(__name__)
path = os.getcwd()
salt = None

try:
    with open(f"{path}/ecity/salt.txt", 'r', encoding="utf-8") as f:
        salt = f.read().encode()
except FileNotFoundError:
    salt = gensalt()
    with open(f"{path}/ecity/salt.txt", 'w', encoding="utf-8") as f:
        f.write(salt.decode())

db_url = 'mysql+mysqldb://User3:password@localhost/ecity'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex().encode()

lm.init_app(app)  # Initialize login manager for `app`
db.init_app(app)  # Initialize database handle for `app`
flask.globals.CURR_USERS = set()

flask.globals.BLOCKED_USERS = []
try:
    with open('ecity/.blocked_users.json', 'r', encoding='utf-8') as f:
        flask.globals.BLOCKED_USERS = json.load(f)
except (FileNotFoundError, JSONDecodeError):
    with open('ecity/.blocked_users.json', 'w', encoding='utf-8') as f:
        json.dump(flask.globals.BLOCKED_USERS, f)

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
    return jsonify({"error": "Not found"}), 404


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
        flask.globals.CURR_USERS.add(user.user_id)
        return user


@lm.unauthorized_handler
def unauthorized_err_401():
    """ Handles unauthorized error """
    logout_user()
    flash('You must be logged in to access the requested resource.', 'error')
    return redirect(url_for('login'))


def block_user(user):
    """ Adds a user to `flask.globals.BLOCKED_USERS` """
    flask.globals.BLOCKED_USERS.append(user.user_id)
    with open('ecity/.blocked_users.json', 'w', encoding='utf-8') as f:
        json.dump(list(set(flask.globals.BLOCKED_USERS)), f)
    return flask.globals.BLOCKED_USERS


def unblock_user(user):
    """ Unblocks a user `flask.globals.BLOCKED_USERS` to file"""
    flask.globals.BLOCKED_USERS.remove(user.user_id)
    with open('ecity/.blocked_users.json', 'w', encoding='utf-8') as f:
        json.dump(list(set(flask.globals.BLOCKED_USERS)), f)
    return flask.globals.BLOCKED_USERS


def authenticate_teacher():
    """
    A helper function that blocks non-teacher account from accessing
    teachers' resources
    """
    try:
        user = current_user
        user.id = user.user_id
    except AttributeError:
        flash('Please login to continue', 'warning')
        return redirect(url_for('login'))

    # Block non-teachers
    if current_user.is_examiner != 'T':
        flash("You are not permitted to view the requested page", 'error')
        return redirect(url_for('student_dashboard', student_id=user.user_id,
                                resource_id=uuid4()))
    return user


def authenticate_student():
    """
    A helper function that blocks non-student account from accessing
    students' resources
    """
    try:
        user = current_user
        user.id = user.user_id
    except AttributeError:
        flash('Please login to continue', 'warning')
        return redirect(url_for('login'))

    # Block non-students
    if current_user.is_student != 'T':
        flash("You are not permitted to view the requested page", 'error')
        return redirect(url_for('dashboard', user_id=user.user_id,
                                resource_id=uuid4()))
    if user.user_id in flask.globals.BLOCKED_USERS:
        flash('Please change default password to continue using this account',
              'warning')
        return redirect(url_for('reset_password', user_id=user.user_id))
    return user


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
    _psword = request.form['_password']

    if psword != _psword:
        flash("The passwords you provided don't match", 'warning')
        return redirect(url_for('sign_up'))

    hashed_password = hashpw(psword.encode(), salt)

    user = User(
        username=u_name, firstname=f_name, lastname=l_name,
        middlename=m_name, email=email, password=hashed_password,
        last_login=datetime.utcnow(), logged_in='T', is_examiner='T'
    )
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
        return redirect(url_for('sign_up', resource_id=uuid4()))
    except Exception:
        db.rollback()
        flash(
            """A server side error just occured. Please notify the
            system administrator at "<i>alexanderikpeama@gmail.com</i>".
            """,
            'error')
        return redirect(url_for('sign_up', resource_id=uuid4()))
    else:
        user = User.query.filter(User.user_id == user.user_id).one()
        user.id = user.user_id
        login_user(user, duration=timedelta(days=30))
        flash(f"Welcome to eCity {user.firstname} {user.lastname}. "
              "If you need help in setting-up your workspace, don't hesitate "
              "to contact our support centre at alexanderikpeama@gmail.com ",
              'success')
        return redirect(
            url_for('dashboard', user_id=user.user_id, resource_id=uuid4())
        )


@app.route('/login', strict_slashes=False)
def login():
    """ Login Page """
    student_login = request.args.get('student_login')
    user = current_user

    if hasattr(user, 'user_id'):
        if user.user_id in flask.globals.BLOCKED_USERS:
            flash(
                'You are logged in. To secure your account, change the'
                ' current default password of your account.',
                'success'
            )
            return redirect(url_for(
                'reset_password', user_id=user.user_id
            ))
        if user.is_student == 'T':
            return redirect(url_for(
                'student_dashboard', student_id=user.user_id
            ))
        elif user.is_examiner == 'T':
            return redirect(url_for(
                'dashboard', user_id=user.user_id
            ))
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
        flash('You have not provided valid login credentials', 'warning')
        return redirect(url_for('login', resource_id=uuid4()))

    try:
        user = User.query.filter(User.username == username).one()
    except Exception as e:
        flash('There is no account associated with the username you provided.',
              'warning')
        return redirect(url_for('login'))
    else:
        hashed_password = hashpw(password.encode(), salt)
        if password == user.password or hashed_password == user.password.encode():  # TODO: remove support for unencrypted passords
            user.id = user.user_id
            if flask.globals.CURR_USERS and \
               user.user_id in flask.globals.CURR_USERS:
                login_user(user, duration=timedelta(days=30))
                if user.user_id in flask.globals.BLOCKED_USERS:
                    flash(
                        'You are logged in. To secure your account, change the'
                        ' current default password of your account.',
                        'success'
                    )
                    return redirect(url_for(
                        'reset_password', user_id=user.user_id
                    ))
                if student_login == 'True':
                    flash('You are already signed-in.', 'success')
                    return redirect(url_for('student_dashboard',
                                            student_id=user.user_id))
                else:
                    if user.is_examiner == 'T':
                        flash('You are already signed-in.', 'success')
                        return redirect(
                            url_for('dashboard', user_id=user.user_id))
                    else:
                        logout_user()
                        flask.globals.CURR_USERS.remove(user.user_id)
                        flash('Please log-in as a student rather.', 'warning')
                        return redirect(url_for('login', resource_id=uuid4()))

            else:
                user.logged_in = 'T'
                user.last_login = datetime.utcnow()
                db.object_session(user).commit()
                login_user(user, duration=timedelta(days=30))
                flask.globals.CURR_USERS.add(user.user_id)
                if user.user_id in flask.globals.BLOCKED_USERS:
                    flash(
                        'You are logged in. To secure your account, change the'
                        ' current default password of your account.',
                        'success'
                    )
                    return redirect(url_for(
                        'reset_password', user_id=user.user_id
                    ))
                if student_login == "True":
                    if user.get_teachers() and user.is_student == 'T':
                        flash('Successfully signed-in', 'success')
                        return redirect(
                            url_for('student_dashboard',
                                    student_id=user.user_id))
                    else:
                        flash(
                            f"""No student account was found with username
                            {user.username}. Try to login as admin instead.""",
                            'warning')
                        logout_user()
                        flask.globals.CURR_USERS.remove(user.user_id)
                        return redirect(url_for('login', resource_id=uuid4()))
                if user.is_examiner == 'T':
                    flash('Successfully signed-in. Welcome back 🙂', 'success')
                    return redirect(url_for('dashboard', user_id=user.user_id))
                else:
                    logout_user()
                    flask.globals.CURR_USERS.remove(user.user_id)
                    flash('Please log-in as a student rather.', 'warning')
                    return redirect(url_for('login', resource_id=uuid4()))
        else:
            flash('The password you entered is incorect. '
                  'Please enter the correct password.', 'warning')
            return redirect(url_for('login', resource_id=uuid4()))


# ------------------ ALL STUDENTS ROUTES HERE --------------------


@app.route('/student/<int:student_id>/dashboard', strict_slashes=False)
@app.route('/student/<int:student_id>/upcoming_exams', strict_slashes=False)
@login_required
def student_dashboard(student_id):
    """ Students dashboard """
    submit_status = request.args.get('ans')
    user = authenticate_student()
    if not isinstance(user, User):
        return user

    # Load exams from all teachers
    all_exams = []
    for teacher in user.get_teachers():
        exams = Exam.query.filter(Exam.user_id == teacher.user_id).all()
        all_exams.extend(exams)

    # filter out all past exams
    uniq_exams = []
    for exam in all_exams:
        start_timestamp = "{}T{}.000000".format(exam.exam_date, exam.start_time)
        end_timestamp = "{}T{}.000000".format(exam.exam_date, exam.end_time)
        exam_start_datetime = datetime.fromisoformat(start_timestamp)
        exam_end_datetime = datetime.fromisoformat(end_timestamp)
        d_time_allowed = timedelta(minutes=exam.time_allowed)
        if (datetime.now() >= exam_start_datetime or \
            datetime.now() + timedelta(minutes=5) >= exam_start_datetime) and \
            datetime.now() <= exam_end_datetime and \
            exam.exam_id not in user.completed_exams():
            # Exam is about to start or is ongoing: Prepare exam instruction page.
            if submit_status not in ['', None]:  # In case of consecutive exams
                flash('Answersheet has been submitted successfully', 'success')
            return render_template('exam_instruction_page.html', exam=exam,
                                   user=user)
        elif datetime.now() < exam_start_datetime:
            exam.exam_end_datetime = exam_end_datetime
            uniq_exams.append(exam)
    if submit_status not in ['', None]:
        flash('Answersheet has been submitted successfully', 'success')
    uniq_exams.sort(key=lambda exam: exam.exam_end_datetime)
    return render_template('student_dashboard.html', user=user,
                           exams=uniq_exams, date=date)


@app.route('/student/<int:student_id>/past_exams', strict_slashes=False)
@login_required
def student_past_exams(student_id):
    """ User dashboard - past exams """
    user = authenticate_student()
    if not isinstance(user, User):
        return user

    # Load exams from all teachers
    all_exams = []
    for teacher in user.get_teachers():
        exams = Exam.query.filter(Exam.user_id == teacher.user_id).all()
        all_exams.extend(exams)

    # filter out any ongoing or future exams
    uniq_exams = []
    answersheet_list = []
    for exam in all_exams:
        timestamp = "{}T{}.000000".format(exam.exam_date, exam.end_time)
        exam_end_datetime = datetime.fromisoformat(timestamp)
        if exam_end_datetime < datetime.now():
            if exam.exam_id in user.completed_exams():  # User wrote this exam
                exam.exam_end_datetime = exam_end_datetime
                exam.score = Score.query.filter(
                    Score.exam_id == exam.exam_id).filter(
                        Score.user_id == int(student_id)
                    ).first()
                uniq_exams.append(exam)
            else:  # User missed this particular exam
                # 1. Create and add a score with value -1
                score = Score(
                    user_id=user.user_id, exam_id=exam.exam_id,
                    score=-1, score_attainable=exam.no_of_questions
                )
                # append exam to uniq_exams
                exam.exam_end_datetime = exam_end_datetime
                exam.score = score
                db.commit()
                uniq_exams.append(exam)

    uniq_exams.sort(key=lambda exam: exam.exam_end_datetime, reverse=True)

    return render_template('student_dashboard_past_exams.html', user=user,
                           exams=uniq_exams, date=date, round=round)


@app.route('/student/<int:student_id>/past_exams/<int:exam_id>',
           strict_slashes=False)
@login_required
def student_past_exam_answersheet(student_id, exam_id):
    """ User dashboard - past exam answersheet """
    user = authenticate_student()
    if not isinstance(user, User):
        return user

    # Load exam answersheet for this student
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    answersheets = AnswerSheet.query.filter(
        AnswerSheet.exam_id == exam_id).filter(
            AnswerSheet.user_id == student_id
        ).all()
    try:
        score = Score.query.filter(
            Score.exam_id == exam_id).filter(
                Score.user_id == student_id
            ).one()
    except NoResultFound:
        score = Score(
            user_id=user.user_id, exam_id=exam.exam_id, score=-1,
            score_attainable=exam.no_of_questions
        )

    return render_template(
        'past_exams/student_past_exam_answersheet.html', user=user, exam=exam,
        score=score, answersheets=answersheets, date=date, round=round
    )


# ------------------ ALL TEACHERS ROUTES HERE --------------------


@app.route('/users/<int:user_id>/dashboard', strict_slashes=False)
@app.route('/users/<int:user_id>/upcoming_exams', strict_slashes=False)
@login_required
def dashboard(user_id):
    """ User dashboard """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    print()
    print()
    print(current_user == user)
    print()
    print()

    exams = Exam.query.filter(Exam.user_id == user_id).all()
    upcoming_exams = []
    ongoing_exams = []
    for exam in exams:
        start_timestamp = "{}T{}.000000".format(exam.exam_date, exam.start_time)
        end_timestamp = "{}T{}.000000".format(exam.exam_date, exam.end_time)
        exam_start_datetime = datetime.fromisoformat(start_timestamp)
        exam_end_datetime = datetime.fromisoformat(end_timestamp)
        if datetime.now() < exam_start_datetime:
            exam.exam_start_datetime = exam_start_datetime
            upcoming_exams.append(exam)
            continue
        temp_tdelta = timedelta(minutes=int(exam.time_allowed))
        if datetime.now() >= exam_start_datetime and \
           datetime.now() <= exam_end_datetime:
            exam.exam_start_datetime = exam_start_datetime
            ongoing_exams.append(exam)
            continue
    upcoming_exams.sort(key=lambda exam: exam.exam_start_datetime)
    ongoing_exams.sort(key=lambda exam: exam.exam_start_datetime)
    return render_template('dashboard.html', user=user,
                           upcoming_exams=upcoming_exams, date=date,
                           ongoing_exams=ongoing_exams)


@app.route('/users/<int:user_id>/past_exams', strict_slashes=False)
@app.route('/users/<int:user_id>/past_exams/<int:exam_id>',
           strict_slashes=False)
@login_required
def past_exams(user_id, exam_id=None):
    """ User dashboard """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    if exam_id is None:
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
    # Load examination where Exam.exam_id == exam_id
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    students = user.get_students()
    no_of_students_who_sat = 0
    no_of_students_who_missed = 0
    for student in students:
        try:
            student.score = Score.query.filter(
                Score.exam_id == exam.exam_id).filter(
                    Score.user_id == student.user_id
                ).one()
        except NoResultFound:
            student.score = Score(
                user_id=student.user_id, exam_id=exam_id, score=-1,
                score_attainable=exam.no_of_questions
            )
            no_of_students_who_missed += 1
        else:
            no_of_students_who_sat += 1

    no_succ = len(
        list(filter(
            lambda student: \
            student.score.score >= student.score.score_attainable / 2, students
        ))
    )

    no_fail = len(
        list(filter(
            lambda student: \
            student.score.score < student.score.score_attainable / 2, students
        ))
    )

    return render_template(
        'past_exams/teacher_past_exam_stat.html', user=user, exam=exam,
        students=students, round=round, len=len, no_succ=no_succ,
        no_fail=no_fail, no_of_students_who_sat=no_of_students_who_sat,
        no_of_students_who_missed=no_of_students_who_missed
    )


@app.route('/user/<int:user_id>/past_exams/<int:exam_id>/<int:student_id>',
           strict_slashes=False)
@login_required
def past_exam_answersheet(user_id, exam_id, student_id):
    """ User dashboard - past exam answersheet """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    # Load exam answersheet for this student
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    student = User.query.filter(User.user_id == student_id).one()
    answersheets = AnswerSheet.query.filter(
        AnswerSheet.exam_id == exam_id).filter(
            AnswerSheet.user_id == student_id
        ).all()
    try:
        score = Score.query.filter(
            Score.exam_id == exam_id).filter(
                Score.user_id == student_id
            ).one()
    except NoResultFound:
        score = Score(
            user_id=student_id, exam_id=exam.exam_id, score=-1,
            score_attainable=exam.no_of_questions
        )

    filename = 'student_past_exam_answersheet_view.html'
    return render_template(
        f'past_exams/student_answersheet_view/{filename}',
        user=user, exam=exam, student=student,
        score=score, answersheets=answersheets, date=date, round=round
    )


@app.route('/users/<int:user_id>/my_students', strict_slashes=False)
@login_required
def my_students(user_id):
    """ User dashboard """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    students = sorted(user.get_students(), key=lambda student: student.user_id,
                      reverse=True)
    return render_template('dashboard_my_students.html', user=user,
                           students=students)


@app.route('/users/<int:user_id>/create_new_student_template',
           methods=['GET'], strict_slashes=False)
@app.route('/users/<int:user_id>/create_new_student', methods=['POST'],
           strict_slashes=False)
@login_required
def create_new_student(user_id):
    """ User dashboard """
    import os

    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    if request.method == 'GET':
        return render_template('add_new_student_template.html', user=user)
    if request.method == 'POST':
        f_name = str(request.form.get('firstname'))
        m_name = str(request.form.get('middlename'))
        l_name = str(request.form.get('lastname'))
        username = str(os.urandom(7)).replace('\\', '').replace(
            'b', '').replace("'", '').replace(' ', '')  # A random username
        default_pass = hashpw('ecity-student-pass'.encode(), salt)
        email = str(request.form.get('email'))
        gender = str(request.form.get('gender'))
        teachers = str(f"{user.user_id},")  # Will be converted to a tuple
        created_at = datetime.utcnow()

        student = User(
            username=username, firstname=f_name, middlename=m_name,
            lastname=l_name, password=default_pass, email=email, gender=gender,
            is_student='T', created_at=created_at, updated_at=created_at,
            logged_in='F', teachers=teachers
        )
        try:
            db.add(student)
        except Exception:
            db.rollback()
            raise
        db.object_session(student).commit()
        block_user(student)
        print(f'blocked student: {student.user_id} {student.firstname} {student.lastname}')
        print(flask.globals.BLOCKED_USERS)
        user.students = f"{user.students},{str(student.user_id)}"
        db.object_session(user).commit()
        flash(
            f"""Successfully created a new student account for
            {student.firstname} {student.lastname} with ID {student.user_id}
            """, 'success'
        )
        return redirect(url_for('my_students', user_id=user_id))


@app.route('/users/<int:user_id>/manage_exams', strict_slashes=False)
@login_required
def manage_exams(user_id):
    """ User dashboard """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    exams = Exam.query.filter(Exam.user_id == user_id).all()
    for exam in exams:
        timestamp = "{}T{}.000000".format(exam.exam_date, exam.end_time)
        exam_end_datetime = datetime.fromisoformat(timestamp)
        if exam_end_datetime < datetime.now():  # Exam has passed
            exam.has_past = True
        else:
            exam.has_past = False
    return render_template('dashboard_manage_exams.html', user=user,
                           date=date, time=time, datetime=datetime,
                           exams=sorted(exams, key=lambda exam: exam.exam_id,
                                        reverse=True))


@app.route('/users/<int:user_id>/manage_exams/create_exam_template',
           methods=['POST'], strict_slashes=False)
@login_required
def create_exam_template(user_id):
    """ Creates an examination """
    user = authenticate_teacher()

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
@login_required
def edit_exam_template(user_id):
    """ Creates a template for setting an examination """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    exam_id = request.args.get('exam_id')
    if not exam_id:
        flash('Exam id not provided.', 'error')
        return redirect(url_for('manage_exams', user_id=user_id))
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    questions = Question.query.filter(Question.exam_id == exam_id).all()

    reschedule = request.args.get('reschedule')
    if reschedule == 'True':  # Delete scores with exam_id == exam.exam_id
        scores = Score.query.filter(
            Score.exam_id == exam.exam_id
        ).all()
        answersheets = AnswerSheet.query.filter(
            AnswerSheet.exam_id == exam.exam_id
        ).all()
        for item in [scores, answersheets]:
            for obj in item:
                obj = db.merge(obj)
                db.delete(obj)
        db.commit()
        print(f"To {user.firstname}: your students'answersheets and scores "
              "have been deleted")
        flash(
            """
            Your students' answersheets and scores for this examination have
            been deleted
            """,
            "success"
        )

    for question in questions:
        answer = Answer.query.filter(
            Answer.question_id == question.question_id).one()
        setattr(question, 'answer', [answer])

    if request.method == 'POST':
        try:
            former_no_of_questions = exam.no_of_questions
            exam.no_of_questions = int(request.form.get('no_of_questions'))
            db.object_session(exam).commit()
        except Exception:
            raise
        else:
            if former_no_of_questions < exam.no_of_questions:
                flash(
                    f"""Successfully increased the number of questions
                    from {former_no_of_questions} to {exam.no_of_questions}
                    """,
                    'success')
            elif former_no_of_questions == exam.no_of_questions:
                flash(
                    f'Nothing changed', 'success')
            else:
                flash(
                    f"""Successfully decreased the number of questions
                    from {former_no_of_questions} to {exam.no_of_questions}
                    """,
                    'success')
    return render_template(
        'manage_exams/edit_exam_template.html', user=user, exam=exam,
        questions=questions, date=date, datetime=datetime, len=len
    )


@app.route('/users/<int:user_id>/manage_exams/delete_exam',
           strict_slashes=False)
@login_required
def delete_exam(user_id):
    """ Creates a template for setting an examination """
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    exam_id = request.args.get('exam_id')
    if not exam_id:
        flash('Exam id not provided.', 'error')
        return redirect(url_for('manage_exams', user_id=user_id))

    user = User.query.filter(User.user_id == user_id).one()
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    course_name = exam.course_name
    questions = Question.query.filter(Question.exam_id == exam_id).all()
    answers = Answer.query.filter(Answer.exam_id == exam_id).all()
    answer_sheets = AnswerSheet.query.filter(
        AnswerSheet.exam_id == exam_id).all()
    scores = Score.query.filter(Score.exam_id == exam_id).all()
    for obj_list in [scores, answer_sheets, answers, questions]:
        for obj in obj_list:
            obj = db.merge(obj)
            db.delete(obj)

    exam = db.merge(exam)
    db.delete(exam)
    db.commit()

    flash(f'Successfully deleted the exam "{course_name}"', 'success')
    return redirect(url_for('manage_exams', user_id=user_id,
                            resource_id=uuid4()))


@app.route('/users/<int:user_id>/manage_exams/<string:instruction>',
           methods=['POST'], strict_slashes=False)
@login_required
def create_or_edit_exam(user_id, instruction):
    """ Creates or edits an examination """
    successful = False
    user = authenticate_teacher()
    if not isinstance(user, User):
        return user

    if instruction == 'create_exam':
        course_name = str(request.form.get('course_name'))
        ex_instruction = str(request.form.get('exam-instruction'))
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
            end_time=end_time, user_id=user_id, instruction=ex_instruction
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
                data = request.form.get(f'Q{i} question-space')
                _dict = {'data': data, 'exam_id': exam.exam_id}
                for opt in available_options:
                    _dict[opt] = request.form.get(
                        f'Q{i}-option-{opt} option-space')
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
                        f'Q{i}-correct_option correct-option-space')).upper()
                    correct_notes = str(request.form.get(
                        f'Q{i}-correct_notes correct-notes-space'
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
                flash("Couldn't create exam something went wrong", 'error')
        return redirect(url_for('manage_exams', user_id=user_id))
    elif instruction == 'edit_exam':
        exam_id = int(request.form.get('exam_id'))
        if not exam_id:
            flash("ERROR: FOR ADIM PURPOSE ONLY: Invalid exam id sent", 'error')
            return redirect(url_for('manage_exams', user_id=user_id))
        exam = Exam.query.filter(Exam.exam_id == exam_id).one()
        try:  # Collect Exam details
            exam.course_name = str(request.form.get('course_name'))
            exam.instruction = str(request.form.get('exam-instruction'))
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
                    data = str(request.form.get(f'Q{i} question-space'))
                    _dict = {'data': data, 'exam_id': exam_id}
                    for opt in available_options:
                        val = request.form.get(
                            f'Q{i}-option-{opt} option-space')
                        if val in ["", 'None']:
                            val = None
                        _dict[opt] = val
                    question = Question(**_dict)
                    db.add(question)
                    db.object_session(question).commit()
                    # Collect correct option
                    correct_option = str(request.form.get(
                        f'Q{i}-correct_option correct-option-space')).upper()
                    if correct_option not in available_options or \
                       getattr(question, correct_option) == None:
                        db.delete(question)
                        exam.no_of_questions -= 1
                        db.commit()
                        flash(
                            f"""You provided an invalid 'correct option' for
                            question {i + 1}. Therefore it was truncated""",
                            'warning')
                        return redirect(
                            url_for('edit_exam_template', user_id=user_id,
                                    exam_id=exam_id)
                        )
                    correct_notes = str(request.form.get(
                        f'Q{i}-correct_notes correct-notes-space'))
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
                    question.data = request.form.get(f'Q{i} question-space')
                    for opt in available_options:
                        val = request.form.get(
                            f'Q{i}-option-{opt} option-space')
                        if val in ["", 'None']:
                            val = None
                        setattr(question, opt, val)
                    db.object_session(question).commit()
                    answer_id = int(request.form.get(f'Q{i}-correct-option-id'))
                    answer = Answer.query.filter(
                        Answer.answer_id == answer_id).one()
                    answer.correct_option = request.form.get(
                        f'Q{i}-correct_option correct-option-space').upper()
                    answer.correct_notes = request.form.get(
                        f'Q{i}-correct_notes correct-notes-space')
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
        return redirect(url_for('manage_exams', user_id=user_id))
    else:
        abort(404)


@app.route('/profiles/<int:user_id>/profile/<string:person_id>',
           methods=['GET', 'POST'], strict_slashes=False)
@login_required
def all_profiles(user_id, person_id):
    """
    Returns or updates the current user's profile page
    or the profile page of the current user's student
    """
    method = request.args.get('method')
    if method and method.upper() == 'DELETE':
        request.method = 'DELETE'

    user = current_user
    user.id = user.user_id
    person = None

    if person_id == 'me':
        person = user
        person.person_id = 'me'
    else:
        try:
            person_id = int(person_id)
        except ValueError:
            abort(404)
        else:
            for student in user.get_students():
                if student.user_id == person_id:
                    student.id = student.user_id
                    person = student
                    person.person_id = person.user_id
                    break
            else:
                abort(404)

    if request.method == 'GET':  # Simply load profile page
        return render_template('profiles/my_profile_page.html', user=user,
                                   person=person)
    elif request.method == 'POST':
        changed = False
        if user.is_examiner != 'T':  # user is a student
            attrs = ['username']
        else:  # user is an admin
            attrs = [
                'username', 'firstname', 'middlename',
                'lastname', 'email'
            ]

        dp = request.files.get('dp')
        if dp and dp.content_type.split('/')[0] == 'image':
            f_ext = dp.filename.split('.')[-1]
            path = f'{getcwd()}/ecity/app/static/images/user_profile_pics'
            dp.save(
                f"{path}/normal_pics/dp-{user.user_id}.{f_ext}"
            )
            dp.close()
            system(  # TODO: Resize image to 50px by 50px
                f"cp -rv {path}/normal_pics/dp-{user.user_id}.{f_ext} "
                f"{path}/compressed_pics/"
            )
            person.dp = f'dp-{user.user_id}.{f_ext}'
            changed = True

        for attr in attrs:
            if str(request.form.get(attr)) and \
               getattr(person, attr) != str(request.form.get(attr)) and \
                   str(request.form.get(attr)) not in ['None', '', None]:
                setattr(person, attr, str(request.form.get(attr)))
                changed = True

        if changed:
            person.updated_at = datetime.utcnow()
            db.object_session(person).commit()
            var = "Your" if user == person else "Your student's"
            flash(f'{var} profile has been updated successfully.', 'success')
            return render_template(
                'profiles/my_profile_page.html', user=user, person=person
            )
        flash('Nothing has changed.', 'success')
        return render_template(
            'profiles/my_profile_page.html', user=user, person=person
        )
    elif request.method == 'DELETE':
        temp_firstname = None
        temp_id = None
        if person.is_student == 'T' and person.is_examiner != 'T':
            temp_firstname = person.firstname
            temp_id = person.user_id
            # delete scores where`score.user_id` == person.user_id
            scores = Score.query.filter(Score.user_id == temp_id).all()
            for score in scores:
                score = db.merge(score)
                db.delete(score)
            # delete answersheets where `answer_sheet.user_id` == person.user_id
            answersheets = AnswerSheet.query.filter(
                AnswerSheet.user_id == temp_id
            ).all()
            for answersheet in answersheets:
                answersheet = db.merge(answersheet)
                db.delete(answersheet)

        if person.is_examiner == 'T':
            temp_firstname = person.firstname
            temp_id = person.user_id
            # Delete students where user.user_id in person.get_students().
            # Firstly delete the student scores, Secondly delete answersheets,
            # Thirdly delete the student
            for student in person.get_students():
                scores = Score.query.filter(  # Delete all scores
                    Score.user_id == student.user_id
                ).all()
                for score in scores:
                    score = db.merge(score)
                    db.delete(score)

                answersheets = AnswerSheet.query.filter(  # Delete all ans_shts
                    AnswerSheet.user_id == student.user_id
                ).all()
                for answersheet in answersheets:
                    answersheet = db.merge(answersheet)
                    db.delete(answersheet)

                path = f'{getcwd()}/ecity/app/static/images/user_profile_pics'
                if student.dp not in ['profile-icon-grey.webp',
                                      'profile-icon.png']:
                    system(f"rm -rfv {path}/normal_pics/{student.dp}")
                    system(f"rm -rfv {path}/compressed_pics/{student.dp}")

                student = db.merge(student)
                db.delete(student)
            print(f'Successfully deleted all students of {temp_firstname}')

            # Delete answers, questions and exams
            exams = Exam.query.filter(Exam.user_id == person.user_id).all()
            for exam in exams:
                questions = Question.query.filter(
                    Question.exam_id == exam.exam_id
                ).all()
                for question in questions:
                    answer = Answer.query.filter(
                        Answer.question_id == question.question_id
                    ).one()
                    answer = db.merge(answer)
                    db.delete(answer)
                    question = db.merge(question)
                    db.delete(question)
                exam = db.merge(exam)
                db.delete(exam)

        # delete person
        person = db.merge(person)
        path = f'{getcwd()}/ecity/app/static/images/user_profile_pics'

        if person.dp not in ['profile-icon-grey.webp', 'profile-icon.png']:
            system(f'rm -rfv {path}/normal_pics/{person.dp}')
            system(f'rm -rfv {path}/compressed_pics/{person.dp}')

        db.delete(person)
        db.commit()
        if user.user_id != temp_id and user.is_examiner == 'T':
            # This block runs only if examiner didn't delete his account
            remaining_students = [std.user_id for std in user.get_students()]
            user.students = str(remaining_students).strip('[]')
            db.object_session(user).commit()
            flash(f"Successfully deleted {temp_firstname}'s account alongside"
                  " all related data.", 'success')
            return redirect(url_for('my_students', user_id=user.user_id))
        else:
            flash("Your account has been successfully deleted alongside all "
                  "related data (Including your student's data).", 'success')
            return redirect(url_for('login'))
    abort(404)


@app.route('/reset_password', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def reset_password():
    """ Resets user password """
    user = current_user
    if request.method == 'GET':
        return render_template('reset_password.html', user=user)

    elif request.method == 'POST':
        curr_password = request.form.get('curr-password')
        new_password = request.form.get('new-password')
        re_new_password = request.form.get('re-new-password')

        if new_password != re_new_password:
            flash("New passwords don't match.", 'warning')
            return render_template('reset_password.html', user=user)

        if hashpw(new_password.encode(), salt) == user.password.encode() or new_password == user.password:  # TODO: remove support for unencrytped passwords
            flash('The new password you provided is the same as your '
                  'current password.', 'warning')
            return render_template('reset_password.html', user=user)

        if hashpw(curr_password.encode(), salt) == user.password.encode() or curr_password == user.password:  # TODO: remove support for unencrytped passwords
            user.updated_at = datetime.utcnow()
            user.password = hashpw(new_password.encode(), salt)
            db.object_session(user).commit()
            print(flask.globals.BLOCKED_USERS)
            if user.user_id in flask.globals.BLOCKED_USERS:
                unblock_user(user)
                print(f'unblocked student: {user.user_id} {user.firstname} {user.lastname}')
                print(flask.globals.BLOCKED_USERS)
            flash('Password successfully changed', 'success')
            return redirect(url_for(
                'all_profiles', user_id=user.user_id, person_id='me'
            ))

        flash('The current password you entered is incorrect.', 'warning')
        return render_template('reset_password.html', user=user)


@app.route('/take_exam', strict_slashes=False, methods=['POST'])
@login_required
def exam_page():
    """ Examination Page. """
    user_id = request.form.get('user_id')
    exam_id = request.form.get('exam_id')
    user = User.query.filter(User.user_id == user_id).one()
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    return render_template('exam_base.html', user=user, exam=exam)


@app.route('/get_exam_questions/<int:exam_id>/', strict_slashes=False)
@login_required
def get_exam_questions(exam_id=None):
    """ Returns all questions for an exam object """
    if exam_id is None:
        abort(404)
    try:
        exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    except NoResultFound:
        return "No question found!", 404
    return exam.all_questions()


@app.route('/student/<int:student_id>/submit_exam/', methods=['POST'],
           strict_slashes=False)
@login_required
def recieve_submitted_exam(student_id=None):
    """
    This endpoint recieves exam answersheets, marks and scores the student
    """
    raw_ans_sheet = dict(request.form)
    user_id = int(request.form.get('user_id'))
    exam_id = int(request.form.get('exam_id'))

    # Do nothing if this student has already written this exam before
    answer_sheets = AnswerSheet.query.filter(
        AnswerSheet.exam_id == exam_id).filter(
            AnswerSheet.user_id == user_id
        ).all()
    if answer_sheets != []:  # i.e. User has already attempted this exam before
        flash('Exam not submitted because you have already concluded this exam'
              ' in the past', 'warning')
        return redirect(url_for('student_dashboard', student_id=user_id))

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
    db.object_session(score).commit()
    return redirect(url_for('student_dashboard', student_id=user_id))  #Not used


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
@login_required
def logout():
    """
    Please not that this logout feature does not yet include support for total
    logout from all browsing sessions across different web clients.
    It's still a work in progress
    """
    user = current_user
    users_ids = flask.globals.CURR_USERS

    for u_id in users_ids:
        if u_id == user.user_id:
            user.last_logout = datetime.utcnow()
            user.logged_in = 'F'
            db.object_session(user).commit()
            flask.globals.CURR_USERS.remove(u_id)
            flash('You have been logged out successfully.', 'success')
            break
    logout_user()
    student_login = request.args.get('student_login')
    if student_login != 'True':
        return redirect(url_for('login', resource_id=uuid4(),
                                student_login='True'))
    else:
        return redirect(url_for('login', resource_id=uuid4()))
