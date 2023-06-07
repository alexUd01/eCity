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
from ecity.models.answer_sheet import AnswerSheet
from ecity.models.score import Score


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
    return jsonify({"error":"Not found"})

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Landing Page """
    # If user is new_user display new_user page
    # else if redirected from login, take old_user to his account
    return "Welcome\n"

@app.route('/sign-up', strict_slashes=False)
def sign_up():
    """ Sigin-up Page """
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
                middlename=m_name, email=email, password=psword)
    try:
        db.add(user)
        db.commit()
    except Exception:
        db.rollback()
        return jsonify({"error": "User already exists.\nDo you want to login?"})
    else:
        return redirect(url_for('dashboard', user_id=user.user_id))

@app.route('/login', strict_slashes=False)
def login():
    """ Login Page """
    return render_template('login.html')

@app.route('/sign-in', strict_slashes=False, methods=['POST'])
def sign_in():
    """ Landing Page """
    username = request.form['username']
    password = request.form['password']
    try:
        user = User.query.filter(User.username == username).one()
    except Exception as e:
        # redirect back to login page with notification
        return jsonify({'error': 'Username does not exist'})
    else:
        if password == user.password:
            return redirect(url_for('dashboard', user_id=user.user_id))
        else:
            # redirect back to login page with notification
            return jsonify({'error': 'User password is incorect'})

@app.route('/users/<int:user_id>/dashboard', strict_slashes=False)
@app.route('/users/<int:user_id>/upcoming_exams', strict_slashes=False)
def dashboard(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard.html', user=user)

@app.route('/users/<int:user_id>/past_exams', strict_slashes=False)
def past_exams(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_past_exams.html', user=user)

@app.route('/users/<int:user_id>/my_students', strict_slashes=False)
def my_students(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_my_students.html', user=user)

@app.route('/users/<int:user_id>/manage_exams', strict_slashes=False)
def manage_exams(user_id):
    """ User dashboard """
    user = User.query.filter(User.user_id == user_id).one()
    return render_template('dashboard_manage_exams.html', user=user)

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

@app.route('/users/<int:user_id>/exams/', methods=['POST'],
           strict_slashes=False)
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
