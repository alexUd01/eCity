@app.route('/student/<int:student_id>/past_exams/<int:exam_id>',
           strict_slashes=False)
@login_required
def student_past_exam_answersheet(student_id, exam_id):
    """ User dashboard - past exam answersheet """
    try:
        user = User.query.filter(User.user_id == student_id).one()
    except NoResusltFound:
        abort(404)
    if user.is_student == 'F' or user.get_teachers() == []:
        flash("You are not permitted to view this page", 'error')
        return redirect(url_for('login', resource_id=uuid4()))

    # Load exam answersheet for this student
    exam = Exam.query.filter(Exam.exam_id == exam_id).one()
    answersheet = AnswerSheet.query.filter(
        AnswerSheet.exam_id == exam_id and AnswerSheet.user_id == user_id
    ).one()

    return render_template('past_exams/student_past_exams.html', user=user,
                           exam=exam, answersheet=answersheet, date=date)
